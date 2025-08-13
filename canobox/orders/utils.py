
# 파일 업로드시 폴더 지정
def printUploadPath(instance, filename):
    from datetime import datetime
    today = datetime.now().strftime('%y%m%d')
    return f"prints/{today}/{filename}"