def nameThumbnail(productName,fileName):
    ext = getExt(fileName)
    return f'{productName}_대표이미지.{ext}'

def namePrintDesign(printDesignName,fileName):
    from datetime import datetime
    today = datetime.now().strftime('%y%m%d')
    ext = getExt(fileName)
    return f'prints/{today}/{printDesignName}.{ext}'

def getExt(fileName: str):
    return fileName.split('.')[-1]
