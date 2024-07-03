
import { useState } from 'react';
import axios from 'axios';

import { UploadSVG } from './SVG';

import './DocUploadPage.css'

function DocUploadPage() {
  const [show, setShow] = useState(false);

  const [file, setFile] = useState([])

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(file);
    if(file != null){
        console.log("submit");
        const formData = new FormData(e.target);
        for (let i = 0; i < file.length; i++) {
            formData.append('file', file[i]);
        }

        axios.post('http://127.0.0.1:5001/upload_doc', formData)
        .then((response) => {
            console.log(response.data);
            alert('上傳成功！')
        })
        .catch((error) => {
            console.error(error);
            alert('上傳失敗 !')
        });
        setShow(false);
        setFile(null);
    }
  };

  let rows = []
  for (let i=0; i < 6; i++) {
    rows.push(<><input id={"app"+(i+1)} type="radio" name="app" /><label htmlFor={"app"+(i+1)}>應用{i+1}</label></>);
  }



    // select option 要 call api 知道有哪些資料庫
    // 上傳前要檢查有沒有選擇資料庫，沒有就 alert 請新增或選擇資料庫
    // 上傳要讓後端知道現在選擇的資料庫
  
  return (
    <>
        <div className='box-center'>
            <div className='box-doc'>
                
                {!show && <><h3>請選擇應用</h3>
                
                <div className='tab_css'>
                    {rows}
                </div>

                <button onClick={() => {setShow(true)}}>
                        下一步
                </button></>}

                {show && <>
                    <h3>點擊圖示，並上傳檔案</h3>
                    <form id="UploadForm" encType="multipart/form-data" onSubmit={handleSubmit}>         
                    <input type="file" id="fileUpload" multiple onChange={(e) => setFile(e.target.files)}/>
                    <label htmlFor="fileUpload">
                            {file.length === 0 && <UploadSVG/> }
                            <ul>
                            {file.length !== 0 && 
                                Array.from(file).map(
                                    (f) => {
                                        return (<li key={f.name}> {f.name} </li>)
                                    }
                                )
                            }
                            </ul>
                    </label>
                </form>
                <div className="" style={{position: 'relative', width: '100%'}}>
                    <button style={{position: 'absolute', left: 0}} onClick={() => {setShow(false)}}>
                        上一步
                    </button>
                    <button variant="primary" type='submit' style={{display: 'block',  margin: '0 auto'}}>
                        上傳
                    </button>
                </div></>}
            </div>
        </div>
    </>
  );
}

export default DocUploadPage;
