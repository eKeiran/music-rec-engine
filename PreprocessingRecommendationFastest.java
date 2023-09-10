import org.python.util.PythonInterpreter;

public class MusicRecEngine {
    public static void main(String[] args) {
        PythonInterpreter interpreter = new PythonInterpreter();

        // execute preprocessing code
        interpreter.exec("C:\Users\keera\Files\SEM IV\Mini Project\MusicRECEngine\preprocessing.py");

        // execute recommendation code
        interpreter.exec("C:\Users\keera\Files\SEM IV\Mini Project\MusicRECEngine\recommender.py");
    }
}

/*  // execute preprocessing code
        interpreter.exec("import pandas as pd\n"
                         + "df = pd.read_csv('data.csv')\n"
                         + "df['feature'] = df['feature'].apply(lambda x: x+1)\n"
                         + "df.to_csv('processed_data.csv', index=False)");

        // execute recommendation code
        interpreter.exec("import pandas as pd\n"
                         + "df = pd.read_csv('processed_data.csv')\n"
                         + "rec = df['recommendation'].unique()[0]\n"
                         + "print('Recommended music:', rec)");*/