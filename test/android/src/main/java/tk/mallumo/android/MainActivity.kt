package tk.mallumo.android

import android.os.*
import androidx.activity.compose.*
import androidx.appcompat.app.*
import androidx.compose.material.*
import tk.mallumo.compose.navigation.*

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                NavigationRoot(Node.AppUI)
            }
        }
    }
}
