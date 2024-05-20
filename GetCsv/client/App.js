import React, { useState } from 'react';
import axios from 'axios';

import './App.css';
import human_pic from './assets/human.jpg';
import ai_pic from './assets/ai.jpg';

import DocUploader from './DocUploader';
import FunctionDialog from './FunctionDialog';

import { ArrowSVG } from './SVG';

import { FunctionDialogContext } from './Context';

// Scroll bar 聊天內容增加就自動向下
// 新增聊天以及歷史紀錄

  

function App() {
	const [userInput, setUserInput] = useState('');
	const [messages, setMessages] = useState([{HumanInput: "123", AiResponse: "456",}]);
	const [loading, setLoading] = useState(false);
	const [analysis, setAnalysis] = useState(false);
	const [query, setQuery] = useState(false);
	

	const handleInputChange = (e) => {
			setUserInput(e.target.value);
		};


	const handleSendMessage = async (e) => {
		e.preventDefault();
		let api = '';
		if(analysis){
			console.log("analysis");
			api = 'http://localhost:5001/get_analysis';
		}
		else if(query){
			console.log("query");
			api = 'http://localhost:5001/get_qa';
		}
		else{
			api ='http://localhost:5001/get_answer';
		}
		if(userInput !== ''){
			setLoading(true);
			setUserInput('')
			const loadingMessage = {
				HumanInput: userInput,
				AiResponse: "請等待",
			};
			setMessages((prevMessages) => [...prevMessages, loadingMessage]);

			axios.post(api, {
				inputText : userInput
			})
			.then(function (response){
				console.log(response.data.response)
				console.log(messages)
				//console.log('status:', response.status)
				var status = response.status;
				const resp = status === 200 ? response.data.response : '暫時無法解析您的問題';
				if (resp === "完成資料搜尋"){
					window.open('/table', '表格資料', 'height=80%');
				}
				//console.log('flaskRes:', resp)
				const newMessage = {
					HumanInput: userInput,
					AiResponse: resp,
				};
				//console.log('this newMessage:', newMessage);
				setMessages((prevMessages) => [...prevMessages.slice(0, -1), newMessage]);
			})
			.catch(function (err){
				alert(`Error: ${err}`);

				const newMessage = {
					HumanInput: userInput,
					AiResponse: "請重新嘗試",
				};
				setMessages((prevMessages) => [...prevMessages.slice(0, -1), newMessage]);
			})
			.finally(() => {
				setLoading(false)
			});
		};
	};



	return (
		<>
			<div className="bg"/>
			<div className="chatbox">
				<div className="chat scrollbar">
					<div className="chat-title">
						聊天室
					</div>
					<div>
						{messages.map((message, index) => (
						<div key={index}>
							{message.HumanInput && 
								<div className="dialog human">
									<div style={{ whiteSpace: 'pre-wrap' }} className="human-box">
										{message.HumanInput}
									</div>
									<img alt="" className="img-profile" 
										src={human_pic} 
									/>
								</div>
							}
							<div className="dialog ai">
								<img alt="" className="img-profile" 
									src={ai_pic} 
								/>
								<div style={{ whiteSpace: 'pre-wrap' }} className="ai-box">
									<span>{message.AiResponse}</span>{loading && (message.AiResponse === '請等待') && <span className="dot"></span>}
								</div>
							</div>
						</div>))}
					</div>
				</div>
				<form 
					className="inputbox" 
					onSubmit={handleSendMessage}
				>	
					<input
							className="msgbox"
							id="content"
							placeholder="Message"
							type="text"
							value={userInput}
							onChange={handleInputChange}
					/>
					{/* <input
						className="balloon"
						type="checkbox"
						checked={Checked}
						onChange={handleCheck}
						data={"資料分析"}
					/> */}
					<DocUploader/>
					<FunctionDialogContext.Provider value={{
						analysis_state: analysis,
						analysis_setter: setAnalysis,
						query_state: query,
						query_setter: setQuery
					}}>
						<FunctionDialog/>
					</FunctionDialogContext.Provider>
					<button
						className= 'btn-send'
						type="submit"
						disabled = {loading}
					>
						<span>Send</span>
						<ArrowSVG/>
					</button>
				</form>

			</div>
		</>
	);
}

export default App;
