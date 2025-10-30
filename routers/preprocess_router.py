# from fastapi import APIRouter, UploadFile, File, Form, HTTPException
# import pandas as pd, os, json

# from services.preprocessing_service import (
#     full_preprocess_pipeline,
#     normalize_columns,
#     standardize_columns
# )

# router = APIRouter()

# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# current_file_path = None


# # ✅ Upload dataset
# @router.post("/upload")
# async def upload_dataset(file: UploadFile = File(...)):
#     global current_file_path

#     file_path = os.path.join(UPLOAD_DIR, file.filename)
#     with open(file_path, "wb") as f:
#         f.write(await file.read())

#     df = pd.read_csv(file_path)
#     current_file_path = file_path

#     return {"message": "File uploaded successfully", 
#             "columns": list(df.columns),
#             "path": file_path}


# # ✅ Apply full preprocessing pipeline
# @router.post("/preprocess/auto")
# async def preprocess_auto():

#     global current_file_path
#     if not current_file_path:
#         raise HTTPException(status_code=400, detail="Upload a file first")

#     df = pd.read_csv(current_file_path)
    
#     df = full_preprocess_pipeline(df)

#     df.to_csv(current_file_path, index=False)

#     return {
#         "message": "✅ Full preprocessing completed (missing values → encoding → outliers)",
#         "path": current_file_path,
#         "columns": list(df.columns)
#     }


# # ✅ Normalize or Standardize
# @router.post("/scale")
# async def scale_data(method: str = Form(...), columns: str = Form(...)):

#     global current_file_path

#     if not current_file_path:
#         raise HTTPException(status_code=400, detail="Upload a file first")

#     df = pd.read_csv(current_file_path)

#     # Parse columns list from string input
#     try:
#         selected_columns = json.loads(columns)
#     except:
#         selected_columns = columns.split(",")

#     if method == "normalize":
#         df = normalize_columns(df, selected_columns)
#     elif method == "standardize":
#         df = standardize_columns(df, selected_columns)
#     else:
#         raise HTTPException(status_code=400, detail="Choose method normalize/standardize")

#     df.to_csv(current_file_path, index=False)

#     return {
#         "message": f"✅ {method} applied to {selected_columns}",
#         "path": current_file_path
#     }



from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
import pandas as pd, os, json

from services.preprocessing_service import (
    full_preprocess_pipeline,
    normalize_columns,
    standardize_columns
)

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

current_file_path = None   # stored original
processed_file_path = None # stored processed file


# ✅ Upload dataset
@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    global current_file_path, processed_file_path

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    df = pd.read_csv(file_path)
    current_file_path = file_path
    processed_file_path = file_path  # initialize same file

    return {
        "message": "File uploaded successfully",
        "columns": list(df.columns),
        "path": file_path
    }


# ✅ Apply full preprocessing pipeline
@router.post("/preprocess/auto")
async def preprocess_auto():

    global current_file_path, processed_file_path
    if not current_file_path:
        raise HTTPException(status_code=400, detail="Upload a file first")

    df = pd.read_csv(current_file_path)
    
    df = full_preprocess_pipeline(df)

    processed_file_path = current_file_path  # overwrite same path
    df.to_csv(processed_file_path, index=False)

    return {
        "message": "✅ Full preprocessing completed (missing values → encoding → outliers)",
        "path": processed_file_path,
        "columns": list(df.columns)
    }


# ✅ Normalize or Standardize
@router.post("/scale")
async def scale_data(method: str = Form(...), columns: str = Form(...)):

    global processed_file_path

    if not processed_file_path:
        raise HTTPException(status_code=400, detail="Upload a file first")

    df = pd.read_csv(processed_file_path)

    try:
        selected_columns = json.loads(columns)
    except:
        selected_columns = columns.split(",")

    if method == "normalize":
        df = normalize_columns(df, selected_columns)
    elif method == "standardize":
        df = standardize_columns(df, selected_columns)
    else:
        raise HTTPException(status_code=400, detail="Choose method normalize/standardize")

    df.to_csv(processed_file_path, index=False)

    return {
        "message": f"✅ {method} applied to {selected_columns}",
        "path": processed_file_path
    }


# ✅ Download processed file
@router.get("/download")
async def download_processed_file():
    global processed_file_path
    
    print(f"Download request received for: {processed_file_path}")
    
    if processed_file_path and os.path.exists(processed_file_path):
        return FileResponse(
            path=processed_file_path,
            filename=os.path.basename(processed_file_path),
            media_type='text/csv'
        )
    else:
        print("❌ No processed file found to download.")
        raise HTTPException(status_code=404, detail="No file has been processed or file not found")
