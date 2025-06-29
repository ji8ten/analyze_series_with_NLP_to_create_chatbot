import gradio as gr
import matplotlib.pyplot as plt
from theme_classifier.theme_classifier import ThemeClassifier

def get_themes(theme_list_str, subtitles_path, save_path):
    theme_list = theme_list_str.split(',')
    theme_classifier = ThemeClassifier(theme_list)
    output_df = theme_classifier.get_themes(subtitles_path, save_path)

    # Remove dialogue from the theme list
    theme_list = [theme for theme in theme_list if theme != 'dialogue']
    theme_list = [theme for theme in theme_list if theme in output_df.columns]
    output_df = output_df[theme_list]

    output_df = output_df.sum().reset_index()
    output_df.columns = ['Theme', 'Score']

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(output_df['Theme'], output_df['Score'], color='skyblue')
    ax.set_xlabel('Score')
    ax.set_title('Series Themes')
    plt.tight_layout()

    return fig


if __name__ == "__main__":
    interface = gr.Interface(
        fn=get_themes,
        inputs=[
            gr.Textbox(label="Theme List (comma separated)"),
            gr.Textbox(label="Subtitles Path"),
            gr.Textbox(label="Save Path (optional, can leave blank)")
        ],
        outputs=gr.Plot(label="Theme Scores Chart")

    )
    interface.launch()
