import React, { useState } from 'react';
import axios from 'axios';

import './App.css';
import human_pic from './assets/human.jpg';
import ai_pic from './assets/ai.jpg';

import DocUploadPage from './DocUploadPage';

import { ArrowSVG } from './SVG';

import {NavBarContext} from './Context';

import NavBar from './NavBar';

// Scroll bar 聊天內容增加就自動向下
// 新增聊天以及歷史紀錄

  

function App() {
	const [userInput, setUserInput] = useState('');
	const [messages, setMessages] = useState([]);
	const [loading, setLoading] = useState(false);

	const [showTab, setTab] = useState([true, false]);
	
	const [analysis, setAnalysis] = useState(false);
	const [check, setCheck] = useState(false);

	const handleInputChange = (e) => {
			setUserInput(e.target.value);
		};


	const handleSendMessage = async (e) => {
		e.preventDefault();
		let api = '';
		let waiting = "";
		if(analysis){
			console.log("analysis");
			setAnalysis(true);
			api = 'http://localhost:5001/get_summary_test';
			waiting = "請等待總結";
		}
		else if(check){
			api = 'http://localhost:5001/get_query';
			waiting = "請等待資料查詢";
		}
		else{
			api ='http://localhost:5001/get_answer';
			// api ='http://localhost:5001/get_test';
			waiting = "請等待回覆";
		}
		if(userInput !== ''){
			setLoading(true);
			setUserInput('');
			let userInputTime = new Date();

			const loadingMessage = {
				HumanInput: userInput,
				AiResponse: waiting,
				HumanTime: userInputTime.toLocaleString(),
				AiTime: "",
			};
			// console.log('this loadingMessage:', loadingMessage);

			setMessages((prevMessages) => [...prevMessages, loadingMessage]);

			axios.post(api, {
				inputText : userInput
			})
			.then(function (response){
				//console.log('status:', response.status)
				var status = response.status;
				const resp = status === 200 ? response.data.response : '暫時無法解析您的問題';
				let result;
				var AiResponseTime ="";
				
				if(response.data.check === 'True'){
					setCheck(true);
				}
				else{
					setCheck(false);
				}

				if (resp === '完成資料搜尋' || resp === '測試'){
					result = '請等待總結'

					window.open('/table', "表格資料", 'height=80%').focus();

					/* 資料分析 START*/
					axios.get(
						'http://localhost:5001/get_summary'
					).then(function (response){
						var status_summary = response.status;
						const resp_summary= status_summary === 200 ? response.data.response : '暫時無法分析資料';
						let AiResponseTime = new Date();

						const newMessage = {
							HumanInput: userInput,
							AiResponse: resp_summary,
							HumanTime: userInputTime.toLocaleString(),
							AiTime: AiResponseTime.toLocaleString(),
						};
						setMessages((prevMessages) => [...prevMessages.slice(0, -1), newMessage]);
					}).catch(function (err){
						alert(`Error: ${err}`);
						let AiResponseTime = new Date();
		
						const newMessage = {
							HumanInput: userInput,
							AiResponse: "請重新嘗試",
							HumanTime: userInputTime.toLocaleString(),
							AiTime: AiResponseTime.toLocaleString(),
						};
						setMessages((prevMessages) => [...prevMessages.slice(0, -1), newMessage]);
					})
					.finally(() => {
						setLoading(false)
					});
					/* 資料分析 END */
				}
				else{
					result = resp;
					setLoading(false);
					AiResponseTime = new Date();
					AiResponseTime = AiResponseTime.toLocaleString()
				}

				const newMessage = {
					HumanInput: userInput,
					AiResponse: result,
					HumanTime: userInputTime.toLocaleString(),
					AiTime: AiResponseTime,
				};
				// console.log('this newMessage:', newMessage);
				setMessages((prevMessages) => [...prevMessages.slice(0, -1), newMessage]);
			})
			.catch(function (err){
				alert(`${err}`);
				setLoading(false);
				let AiResponseTime = new Date();

				const newMessage = {
					HumanInput: userInput,
					AiResponse: "請重新嘗試",
					HumanTime: userInputTime.toLocaleString(),
					AiTime: AiResponseTime.toLocaleString(),
				};
				setMessages((prevMessages) => [...prevMessages.slice(0, -1), newMessage]);
			})
		};
	};



	return (
		<>
			<div className="bg"/>
			<NavBarContext.Provider value={{
				tab_setter: setTab,
			}}>
				<NavBar/>
			</NavBarContext.Provider>
			{showTab[0] && <div className="chatbox">
				<div className="chat scrollbar">
					<div className="chat-title">
						聊天室
					</div>
					<div>
						{messages.map((message, index) => (
						<div key={index}>
							{message.HumanInput && 
								<>
								<div className="humanTime">{message.HumanTime}</div>
								<div className="dialog human">
									<div style={{ whiteSpace: 'pre-wrap' }} className="human-box">
										{message.HumanInput}
									</div>
									<img alt="" className="img-profile" 
										src={human_pic} 
									/>
								</div>
								</>
							}
							<div className="AiTime">{message.AiTime}</div>
							<div className="dialog ai">
								<img alt="" className="img-profile" 
									src={ai_pic} 
								/>
								<div style={{ whiteSpace: 'pre-wrap' }} className="ai-box">
									<span>{message.AiResponse}</span>{loading && (message.AiResponse.includes("請等待")) && <span className="dot"></span>}
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
					/>
					<DocUploader/>
					<FunctionDialogContext.Provider value={{
						analysis_state: analysis,
						analysis_setter: setAnalysis,
						query_state: query,
						query_setter: setQuery
					}}>
						<FunctionDialog/>
					</FunctionDialogContext.Provider> */}
					<button
						className= 'btn-send'
						type="submit"
						disabled = {loading}
					>
						<span>Send</span>
						<ArrowSVG/>
					</button>
				</form>
			</div>}
			{showTab[1] && <DocUploadPage/>}
		</>
	);
}

export default App;
