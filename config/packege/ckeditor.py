from config.env import env


## For CkEditor
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        # 'width': 1200,        
        # 'height': 800,
        'extraPlugins': ','.join(
            [
                # 'widget',

                # 'html5video',  ## For HTML5 video added with your CkEditors
                # 'youtube',  ## For YouTube video added with your CkEditors

            ]
        ),
    },
}