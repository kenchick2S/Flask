import { useContext, useRef} from 'react'

import './FunctionDialog.css'
import { CopilotSVG, CopilotSVG2 } from './SVG';
import { FunctionDialogContext } from './Context';

export default function FunctionDialog(){

    const context = useContext(FunctionDialogContext);

    const dialog = useRef(null);
    const dialogBox = useRef(null);

    const dialogControl = () => {
        dialog.current.style.display = (dialog.current.style.display !== 'none' ? 'none' : 'block');

        const handleClick = (e) => {
            if(!dialogBox.current.contains(e.target)){
              dialog.current.style.display = "none";
              window.removeEventListener("click", handleClick);
            }
        }
        window.addEventListener("click", handleClick);
        
    }


    return(
        <div ref={dialogBox} className="testbox1">
                {/* <div style={{width: '100vw', height: '100vh', position: 'fixed', top: 0, left: 0, zIndex: 2, pointerEvents: "none"}} onClick={() => setClicked(!Clicked)}></div> */}
                <div ref={dialog} role="dialog" className="dialog1" style={{display: 'none'}}>
                    <div style={{borderBottom: '1px solid', lineHeight: '18px', fontSize: '18px', textAlign: 'left', padding: '5px'}}>功能選單:</div> 
                    <div><input type="checkbox" checked={context.analysis_state} onChange={() => context.analysis_setter(!context.analysis_state)}></input><span>資料分析</span></div>
                    <div><input type="checkbox" checked={context.query_state} onChange={() => context.query_setter(!context.query_state)}></input><span>資料查詢</span></div>
                </div>
            <div role="button" className="btn1" onClick={() => dialogControl()}><CopilotSVG/><CopilotSVG2/></div>
        </div>
    )
}
