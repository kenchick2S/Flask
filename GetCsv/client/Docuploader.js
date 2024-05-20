import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import axios from 'axios';

import { CopilotClipSVG } from './SVG';

import './DocUploader.css'

function DocUploader() {
  const [show, setShow] = useState(false);

  const [file, setFile] = useState(null)

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

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



  
  return (
    <>
      <div className='box-upload'>
        <div role='button' className="btn-modals" onClick={handleShow}>
          <CopilotClipSVG/>
        </div>
      </div>

      <Modal show={show} onHide={handleClose}>
        <form id="formfile" encType="multipart/form-data" onSubmit={handleSubmit}>
            <Modal.Header closeButton>
            <Modal.Title>
              檔案上傳:
            </Modal.Title>
            </Modal.Header>
            <Modal.Body>            
                <input type="file" id="fileUpload" multiple onChange={(e) => setFile(e.target.files)}/>
                <ul>
                {file != null &&
                    Array.from(file).map(
                        (f) => {
                            return (<li key={f.name}> {f.name} </li>)
                        }
                    )
                }
                </ul>
            </Modal.Body>
            <Modal.Footer>
            <label type="button" htmlFor="fileUpload">
                選擇檔案
            </label>
            <Button variant="primary" type='submit'>
                上傳
            </Button>
            </Modal.Footer>
        </form>
      </Modal>
    </>
  );
}

export default DocUploader;
