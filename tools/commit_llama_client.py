import sys
import os
import subprocess
import json
import time
import urllib.request
import urllib.error

SYSTEM_PROMPT = """You are an expert software engineer. Generate a highly detailed git commit message using Conventional Commits format.

Structure:
1. Header: <type>(<scope>): <short description>
2. Body: A detailed bulleted list explaining the logic changes, the motivation (why), and any architectural impacts. Contrast old vs new behavior.
3. Footer: Note any BREAKING CHANGES. Do NOT include issue IDs, JIRA references, or 'Related Issues' sections.

Rules:
- Use imperative mood.
- Be technical and precise.
- Do not use conversational filler.
- Do not include any Jira/Issue tracking information.
- Output ONLY the raw commit message. Do NOT wrap it in markdown code blocks (e.g., no ``` or ```conventional_commit)."""

CHUNK_SYSTEM_PROMPT = """You are an expert software engineer.
Analyze the git diff for this subset of files and generate a detailed bulleted list of changes.
Explain the logic changes, the motivation (why), and contrast old vs new behavior.
Output ONLY the raw bulleted list of changes. Do NOT include header, footer, or any conversational filler. Do NOT wrap in markdown code blocks."""

FINAL_SYSTEM_PROMPT = """You are an expert software engineer.
Generate a cohesive Conventional Commit message based on the provided summaries of changes.

Structure:
1. Header: <type>(<scope>): <short description>
2. Body: A detailed, consolidated bulleted list explaining the logic changes, the motivation (why), and any architectural impacts.
3. Footer: Note any BREAKING CHANGES. Do NOT include issue IDs, JIRA references, or 'Related Issues' sections.

Rules:
- Use imperative mood.
- Be technical and precise.
- Do not use conversational filler.
- Do not include any Jira/Issue tracking information.
- Output ONLY the raw commit message. Do NOT wrap it in markdown code blocks."""

def check_alive():
    url = "http://localhost:9090/v1/chat/completions"
    data = json.dumps({
        "messages": [{"role": "user", "content": "ping"}],
        "max_tokens": 1
    }).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.getcode() == 200:
                response.read()
                return True
    except Exception:
        pass
    return False

def ensure_llama_service():
    # 1. Check if llamaDS.service is running. If running, stop it first
    print("Checking llamaDS.service status...", flush=True)
    status_ds = subprocess.run(["sudo", "systemctl", "status", "llamaDS.service"], capture_output=True, text=True)
    if status_ds.returncode == 0:
        print("llamaDS.service is running. Stopping llamaDS.service...", flush=True)
        try:
            subprocess.run(["sudo", "systemctl", "stop", "llamaDS.service"], check=True)
            print("llamaDS.service stopped successfully.", flush=True)
        except subprocess.CalledProcessError as e:
            print(f"Warning/Error stopping llamaDS.service: {e}", file=sys.stderr)

    # 2. Validate if llamaJB.service is running using sudo systemctl status llamaJB.service
    print("Checking llamaJB.service status...", flush=True)
    status_res = subprocess.run(["sudo", "systemctl", "status", "llamaJB.service"], capture_output=True, text=True)
    if status_res.returncode != 0:
        print("llamaJB.service is not running. Starting it...", flush=True)
        try:
            subprocess.run(["sudo", "systemctl", "start", "llamaJB.service"], check=True)
            print("llamaJB.service started. Waiting for initialization...", flush=True)
            time.sleep(5)
        except subprocess.CalledProcessError as e:
            print(f"Error starting llamaJB.service: {e}", file=sys.stderr)
            sys.exit(1)
            
    # 3. Validation alive request. If fail, then restart: sudo systemctl restart llamaJB.service
    if not check_alive():
        print("Llama service alive check failed. Restarting llamaJB.service...", flush=True)
        try:
            subprocess.run(["sudo", "systemctl", "restart", "llamaJB.service"], check=True)
            print("llamaJB.service restarted. Waiting for initialization...", flush=True)
            for i in range(15):
                time.sleep(2)
                if check_alive():
                    print("Llama service is alive and ready.", flush=True)
                    return
            print("Error: Llama service failed alive check after restart.", file=sys.stderr)
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"Error restarting llamaJB.service: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Llama service is alive and ready.", flush=True)

def run_git(args, cwd):
    try:
        return subprocess.check_output(['git'] + args, cwd=cwd, text=True).strip()
    except subprocess.CalledProcessError:
        return ""

LLAMA_CONTEXT_SIZE = 32768
MAX_DIFF_TOKENS = 28000

def count_tokens(text):
    if not text:
        return 0
    url = "http://localhost:9090/tokenize"
    data = json.dumps({"content": text}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.getcode() == 200:
                res_obj = json.loads(response.read().decode("utf-8"))
                if "tokens" in res_obj:
                    return len(res_obj["tokens"])
    except Exception:
        pass
    # Fallback heuristic: code and diffs have approx 3.2 characters per token
    return max(1, int(len(text) / 3.2))

def tokenize_text(text):
    if not text:
        return []
    url = "http://localhost:9090/tokenize"
    data = json.dumps({"content": text}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.getcode() == 200:
                res_obj = json.loads(response.read().decode("utf-8"))
                if "tokens" in res_obj:
                    return res_obj["tokens"]
    except Exception:
        pass
    return None

def detokenize_tokens(tokens):
    url = "http://localhost:9090/detokenize"
    data = json.dumps({"tokens": tokens}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.getcode() == 200:
                res_obj = json.loads(response.read().decode("utf-8"))
                if "content" in res_obj:
                    return res_obj["content"]
    except Exception:
        pass
    return None

def truncate_to_max_tokens(diff_text, max_tokens=MAX_DIFF_TOKENS):
    tokens = tokenize_text(diff_text)
    if tokens is not None:
        if len(tokens) <= max_tokens:
            return diff_text, False
        print(f"TRUNCATING SINGLE FILE DIFF: {len(tokens)} tokens -> {max_tokens} tokens", flush=True)
        truncated_str = detokenize_tokens(tokens[:max_tokens])
        if truncated_str is not None:
            return truncated_str + "\n\n... [DIFF TRUNCATED DUE TO MODEL LIMITS] ...", True
    max_chars = int(max_tokens * 3.2)
    if len(diff_text) > max_chars:
        print(f"TRUNCATING SINGLE FILE DIFF: {len(diff_text)} chars -> {max_chars} chars (heuristic)", flush=True)
        return diff_text[:max_chars] + "\n\n... [DIFF TRUNCATED DUE TO MODEL LIMITS] ...", True
    return diff_text, False

def get_single_diff(f, cwd, staged=False):
    if not f.strip():
        return ""
    args = ['diff', '--ignore-submodules']
    if staged:
        args.append('--cached')
    args.extend(['--', f.strip()])
    return run_git(args, cwd)

def get_diffs(files, cwd, staged=False, diffs_cache=None):
    if isinstance(files, str):
        file_list = [f.strip() for f in files.splitlines() if f.strip()]
    else:
        file_list = [f.strip() for f in files if f.strip()]
    diff_text = []
    for i, f in enumerate(file_list, 1):
        if diffs_cache is not None and f in diffs_cache:
            d = diffs_cache[f]
        else:
            d = get_single_diff(f, cwd, staged=staged)
        if d:
            diff_text.append(f"--- FILE {i}: {f} ---\n{d}")
    return "\n\n".join(diff_text)

class DirNode:
    def __init__(self, path):
        self.path = path
        self.files = []
        self.children = {}

def chunk_node_files(files, file_tokens, bmax=10, max_tokens=MAX_DIFF_TOKENS):
    chunks = []
    current_chunk = []
    current_tokens = 0
    
    for f in files:
        tokens = file_tokens.get(f, 0) if file_tokens else 0
        
        # If this single file alone exceeds max_tokens, it gets its own single-file chunk
        if tokens >= max_tokens:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = []
                current_tokens = 0
            chunks.append([f])
            continue
            
        # If adding this file would exceed bmax files or max_tokens, flush current chunk
        if current_chunk and (len(current_chunk) >= bmax or current_tokens + tokens > max_tokens):
            chunks.append(current_chunk)
            current_chunk = [f]
            current_tokens = tokens
        else:
            current_chunk.append(f)
            current_tokens += tokens
            
    if current_chunk:
        chunks.append(current_chunk)
        
    return chunks

def process_node(node, file_tokens=None, bmax=10, max_tokens=MAX_DIFF_TOKENS, is_root=False):
    all_chunks = []
    
    # Bottom-up: process children first
    for child in node.children.values():
        child_chunks, _ = process_node(child, file_tokens=file_tokens, bmax=bmax, max_tokens=max_tokens, is_root=False)
        all_chunks.extend(child_chunks)
        
    # Chunk this node's files, respecting both bmax and token size to avoid truncating multiple files
    if node.files:
        if file_tokens is not None:
            node_chunks = chunk_node_files(node.files, file_tokens, bmax=bmax, max_tokens=max_tokens)
            all_chunks.extend(node_chunks)
        else:
            for i in range(0, len(node.files), bmax):
                all_chunks.append(node.files[i:i+bmax])
            
    return all_chunks, []

def chunk_files(files_list, file_tokens=None, bmax=10, max_tokens=MAX_DIFF_TOKENS):
    root = DirNode("")
    for f in files_list:
        if not f.strip(): continue
        parts = f.split('/')
        curr = root
        for part in parts[:-1]:
            if part not in curr.children:
                curr.children[part] = DirNode(os.path.join(curr.path, part) if curr.path else part)
            curr = curr.children[part]
        curr.files.append(f)
        
    final_chunks, _ = process_node(root, file_tokens=file_tokens, bmax=bmax, max_tokens=max_tokens, is_root=True)
    return final_chunks


def detect_repetition_loop(content, min_len=8, max_repeats=3):
    if len(content) < min_len * max_repeats:
        return False
    # 1. Exact substring repetition check with a larger window (e.g. up to 1000 chars)
    max_check_len = min(1000, len(content) // max_repeats + 1)
    for length in range(min_len, max_check_len):
        pattern = content[-length:]
        is_repeat = True
        for r in range(1, max_repeats):
            start = -length * (r + 1)
            end = -length * r
            if content[start:end] != pattern:
                is_repeat = False
                break
        if is_repeat:
            return True

    # 2. Line-level repetition check (detects single or multiple lines repeated consecutively)
    lines = [l.strip() for l in content.splitlines() if l.strip()]
    num_lines = len(lines)
    if num_lines >= max_repeats:
        max_block_size = min(20, num_lines // max_repeats)
        for block_size in range(1, max_block_size + 1):
            pattern_lines = lines[-block_size:]
            is_repeat = True
            for r in range(1, max_repeats):
                start = -block_size * (r + 1)
                end = -block_size * r
                chunk = lines[start:end]
                if chunk != pattern_lines:
                    is_repeat = False
                    break
            if is_repeat:
                return True

    return False

def generate_message(diffs, system_prompt=SYSTEM_PROMPT):
    if not diffs: return "", False
    
    # Token limit management (llamaJB.service context is 32768 tokens)
    diff_tokens = count_tokens(diffs)
    if diff_tokens > MAX_DIFF_TOKENS:
        print(f"TRUNCATING DIFF: {diff_tokens} tokens -> {MAX_DIFF_TOKENS} tokens", flush=True)
        diffs, _ = truncate_to_max_tokens(diffs, MAX_DIFF_TOKENS)

    url = "http://localhost:9090/v1/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyze the following git diff and output the requested commit message:\n\n{diffs}"}
        ],
        "temperature": 0.6,
        "top_p": 0.90,
        "stream": True
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    full_content = ""
    loop_detected_overall = False
    
    print("GENERATING MESSAGE...", flush=True)
    try:
        with urllib.request.urlopen(req) as response:
            for line in response:
                line = line.decode('utf-8').strip()
                if not line:
                    continue
                if line.startswith("data: "):
                    data_str = line[len("data: "):]
                    if data_str == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data_str)
                        choices = chunk.get("choices", [])
                        if choices:
                            delta = choices[0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                sys.stdout.write(content)
                                sys.stdout.flush()
                                full_content += content
                                if detect_repetition_loop(full_content):
                                    print("\n[REPETITION LOOP DETECTED, DEDUPLICATING AND CONTINUING]")
                                    loop_detected_overall = True
                                    break
                    except json.JSONDecodeError:
                        pass
    except urllib.error.HTTPError as e:
        print(f"\nError communicating with local llama service: {e}")
        try:
            print("Response body:", e.read().decode("utf-8"))
        except Exception:
            pass
    except Exception as e:
        print(f"\nError communicating with local llama service: {e}")
    
    # Deduplicate trailing repeated lines if loop occurred
    if loop_detected_overall and full_content:
        lines = full_content.splitlines()
        deduped = []
        for l in lines:
            if not deduped or l != deduped[-1]:
                deduped.append(l)
        full_content = "\n".join(deduped)

    print("\n" + "="*40)
    return full_content.strip(), loop_detected_overall

def is_svg_file(filepath):
    normalized = filepath.replace('\\', '/')
    parts = normalized.split('/')
    if len(parts) >= 2 and parts[-2] == 'svg':
        return filepath.endswith('.kt') or filepath.endswith('.svg')
    return False

def get_file_status(f, cwd):
    status_output = run_git(['status', '--porcelain', '--', f], cwd)
    if status_output:
        status_code = status_output[:2].strip()
        if 'D' in status_code:
            return 'removed'
        elif 'A' in status_code or '??' in status_code:
            return 'added'
        else:
            return 'modified'
    return 'modified'

def append_svg_bullets(commit_msg, svg_bullets):
    if not commit_msg:
        commit_msg = "feat(svg): update SVG assets"
    
    lines = commit_msg.splitlines()
    if len(lines) == 1:
        return commit_msg + "\n\n" + "\n".join(svg_bullets)
        
    if len(lines) > 1 and lines[1].strip() != "":
        lines.insert(1, "")
        
    footer_idx = len(lines)
    for idx, line in enumerate(lines):
        if idx > 0 and (line.startswith("BREAKING CHANGE") or line.startswith("BREAKING-CHANGE")):
            footer_idx = idx
            break
            
    inserted_lines = lines[:footer_idx]
    if len(inserted_lines) == 2 and inserted_lines[1].strip() == "":
        inserted_lines.extend(svg_bullets)
    else:
        inserted_lines.extend(svg_bullets)
        
    inserted_lines.extend(lines[footer_idx:])
    return "\n".join(inserted_lines)

def generate_commit_message(files_text, staged, target_dir, bmax=10):
    files_list = [f.strip() for f in files_text.splitlines() if f.strip()]
    if not files_list:
        return "", []
        
    svg_files = [f for f in files_list if is_svg_file(f)]
    normal_files = [f for f in files_list if not is_svg_file(f)]
    
    svg_bullets = []
    if svg_files:
        for f in svg_files:
            basename = os.path.basename(f)
            status = get_file_status(f, target_dir)
            action = 'removed' if status == 'removed' else 'added'
            svg_bullets.append(f"- SVG {basename} {action}")
            
    if not normal_files:
        # Only SVG files changed, generate message directly without AI
        return "\n\n".join([
            "feat(svg): update SVG assets",
            "\n".join(svg_bullets)
        ]), []

    format_sh = os.path.expanduser("~/.local/share/JetBrains/Toolbox/apps/android-studio/bin/format.sh")
    if os.path.exists(format_sh):
        for f in normal_files:
            if get_file_status(f, target_dir) != 'removed':
                file_absolute_path = os.path.abspath(os.path.join(target_dir, f))
                print(f"FORMATTING: {f}")
                subprocess.run([format_sh, "-allowDefaults", file_absolute_path], capture_output=True)
                if staged:
                    subprocess.run(['git', 'add', f], cwd=target_dir)
        
    commit_msg = ""
    skipped_files = []
    
    # Pre-calculate file diffs and token counts to avoid truncating multiple files
    print("CALCULATING DIFF SIZES AND TOKENS...", flush=True)
    file_diffs = {}
    file_tokens = {}
    for f in normal_files:
        d = get_single_diff(f, target_dir, staged=staged)
        file_diffs[f] = d
        file_tokens[f] = count_tokens(f"--- FILE: {f} ---\n{d}" if d else "")
        print(f"  - {f}: ~{file_tokens[f]} tokens", flush=True)
        
    total_tokens = sum(file_tokens.values())
    print(f"TOTAL TOKENS: ~{total_tokens} (Per-chunk limit: {MAX_DIFF_TOKENS}, bmax: {bmax})", flush=True)
    
    if len(normal_files) <= bmax and total_tokens <= MAX_DIFF_TOKENS:
        # For small diffs (<= bmax files and fitting within token limit), generate directly to be fast
        diffs = get_diffs(normal_files, target_dir, staged=staged, diffs_cache=file_diffs)
        commit_msg, loop_detected = generate_message(diffs, SYSTEM_PROMPT)
        if loop_detected:
            skipped_files.extend(normal_files)
            commit_msg = ""
    else:
        # For diffs exceeding bmax or token limits, chunk by directory and calculate sizes to avoid truncating multiple files
        chunks = chunk_files(normal_files, file_tokens=file_tokens, bmax=bmax, max_tokens=MAX_DIFF_TOKENS)
        print(f"SPLITTING DIFF INTO {len(chunks)} CHUNKS BY DIRECTORY/SIZE...")
        
        summaries = []
        for i, chunk in enumerate(chunks, 1):
            chunk_tokens = sum(file_tokens.get(f, 0) for f in chunk)
            print(f"\n--- PROCESSING CHUNK {i}/{len(chunks)} ({len(chunk)} files, ~{chunk_tokens} tokens) ---")
            for f in chunk:
                print(f"  - {f} (~{file_tokens.get(f, 0)} tokens)")
            chunk_diffs = get_diffs(chunk, target_dir, staged=staged, diffs_cache=file_diffs)
            
            # If a single file alone exceeds MAX_DIFF_TOKENS, only truncate that single file
            if len(chunk) == 1 and chunk_tokens > MAX_DIFF_TOKENS:
                print(f"  [Single file {chunk[0]} diff exceeds {MAX_DIFF_TOKENS} tokens, truncating single file diff]")
                chunk_diffs, _ = truncate_to_max_tokens(chunk_diffs, MAX_DIFF_TOKENS)
                
            chunk_summary, loop_detected = generate_message(chunk_diffs, CHUNK_SYSTEM_PROMPT)
            if loop_detected:
                skipped_files.extend(chunk)
                continue
            if chunk_summary:
                summaries.append(chunk_summary)
                
        if summaries:
            combined_summaries = "\n\n".join(summaries)
            print("\n========================================")
            print("GENERATING FINAL CONSOLIDATED COMMIT MESSAGE...")
            commit_msg, loop_detected = generate_message(combined_summaries, FINAL_SYSTEM_PROMPT)
            if loop_detected:
                commit_msg = "feat: update multiple files (summaries truncated due to looping)\n\n" + combined_summaries
            
    if svg_bullets:
        commit_msg = append_svg_bullets(commit_msg, svg_bullets)
        
    return commit_msg, skipped_files

def main():
    bmax = 10
    if "-bmax" in sys.argv:
        try:
            idx = sys.argv.index("-bmax")
            bmax = int(sys.argv[idx + 1])
            sys.argv.pop(idx + 1)
            sys.argv.pop(idx)
        except (ValueError, IndexError):
            pass

    # pop unused args to avoid breaking target_dir parsing
    if "--model" in sys.argv:
        try:
            idx = sys.argv.index("--model")
            sys.argv.pop(idx + 1)
            sys.argv.pop(idx)
        except (ValueError, IndexError):
            pass
    if "--gpu" in sys.argv:
        try:
            idx = sys.argv.index("--gpu")
            sys.argv.pop(idx)
        except ValueError:
            pass

    if len(sys.argv) > 2:
        target_dir = sys.argv[2]
    elif len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = os.getcwd()

    if not os.path.isdir(target_dir):
        print(f"Error: {target_dir} is not a directory.")
        sys.exit(1)

    os.chdir(target_dir)
    print(f"WR: {target_dir}")
    print(f"BMAX: {bmax}")

    # Ensure llamaJB.service is running and alive
    ensure_llama_service()

    try:
        # 0. Initial staged state
        initial_staged = run_git(['diff', '--cached', '--name-only', '--ignore-submodules'], target_dir)
        
        # 1. Check for unstaged files
        unstaged = run_git(['diff', '--name-only', '--ignore-submodules'], target_dir)
        summary = ""
        was_staged_now = False
        all_skipped_files = []

        if unstaged:
            print("========================================")
            print("UNSTAGED FILES DETECTED:")
            for f in unstaged.splitlines(): print(f"  - {f}")
            
            summary, skipped = generate_commit_message(unstaged, staged=False, target_dir=target_dir, bmax=bmax)
            all_skipped_files.extend(skipped)
            
            for f in unstaged.splitlines():
                if f in skipped:
                    print(f"Skipping staging of looping file: {f}")
                    continue
                subprocess.run(['git', 'add', f], cwd=target_dir)
            print("Files staged automatically.")
            was_staged_now = True

        # 2. Proceed with staged files
        staged = run_git(['diff', '--cached', '--name-only', '--ignore-submodules'], target_dir)
        if not staged:
            print("No staged changes to commit. Exiting.")
            if all_skipped_files:
                print("\nFILES NOT COMMITTED DUE TO LOOPING:")
                for f in all_skipped_files: print(f"  - {f}")
            return

        commit_msg = ""
        if was_staged_now and not initial_staged:
            print("Using generated summary for commit message.")
            commit_msg = summary
        else:
            print("========================================")
            print("STAGED FILES TO COMMIT:")
            for f in staged.splitlines(): print(f"  - {f}")
            commit_msg, skipped = generate_commit_message(staged, staged=True, target_dir=target_dir, bmax=bmax)
            all_skipped_files.extend(skipped)
            if skipped:
                for f in skipped:
                    print(f"Unstaging looping file: {f}")
                    subprocess.run(['git', 'reset', 'HEAD', '--', f], cwd=target_dir)

        if not commit_msg:
            staged = run_git(['diff', '--cached', '--name-only', '--ignore-submodules'], target_dir)
            if not staged:
                print("Error: Failed to generate commit message and no staged files remaining.")
                if all_skipped_files:
                    print("\nFILES NOT COMMITTED DUE TO LOOPING:")
                    for f in all_skipped_files: print(f"  - {f}")
                return
            else:
                commit_msg = "feat: update multiple files (looping occurred in some chunks)"

        confirm = input("COMMIT THESE CHANGES? (Y/n) [Y]: ").strip().lower() or 'y'
        if confirm == 'y':
            git_dir = run_git(['rev-parse', '--git-dir'], target_dir)
            if not git_dir:
                print("Error: Could not resolve git directory. Not a git repository?")
                sys.exit(1)
            
            if not os.path.isabs(git_dir):
                git_dir = os.path.abspath(os.path.join(target_dir, git_dir))
                
            msg_file = os.path.join(git_dir, "COMMIT_EDITMSG_LL_TMP")
            with open(msg_file, 'w') as f:
                f.write(commit_msg)
            subprocess.run(['git', 'commit', '-F', msg_file], cwd=target_dir)
            if os.path.exists(msg_file): os.remove(msg_file)
            print("DONE")
            if all_skipped_files:
                print("\nFILES NOT COMMITTED DUE TO LOOPING:")
                for f in all_skipped_files: print(f"  - {f}")
        else:
            print("ABORTED")
            if all_skipped_files:
                print("\nFILES NOT COMMITTED DUE TO LOOPING:")
                for f in all_skipped_files: print(f"  - {f}")
    except Exception as e:
        print(f"Error occurred in main loop: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
