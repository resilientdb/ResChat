import React, {Component, useCallback, useEffect, useRef, useState} from 'react';
import { useNavigate, Link } from 'react-router-dom';
import resdbLogo from "./resource/resilientdb_logo.svg";
import ucdavisLogo from "./resource/ucdavis_logo.png";
// import logo from './logo.svg';
import {Avatar, List, Button, Input, Image, message, Space} from 'antd';
import './Chat.css';
import reschatLogo from "./resource/reschat_logo.svg";


function Chat (){
    const [inputMessage, setInputMessage] = useState("");
    const [sendButtonLoading, setSendButtonLoading] = useState(false);
    const [historyButtonLoading, setHistoryButtonLoading] = useState(false);
    const[currentChattingFriend, setCurrentChattingFriend] = useState(null);
    const[myChatData, setMyChatData] = useState([])
    const [isChat, setIsChat] = useState(true);
    const chatListRef = useRef(null)
    const back = useNavigate();
    const inputRef = useRef(null);
    const[friendData, setFriendData] = useState([])
    const addFriendUsernameRef = useRef(null);
    const addFriendNicknameRef = useRef(null);
    const inputBoxRef = useRef(null)
    const [messageApi, contextHolder] = message.useMessage();
    const success = (text) => {
        messageApi.open({
            type: 'success',
            content: text,
        });
    };
    const error = (text) => {
        messageApi.open({
            type: 'error',
            content: text,
        });
    };


    useEffect(()=>{
        fetch(`http://localhost:8080/friendList`).then(
            response => {
                return response.json()
            }
        ).then(
            data => {
                // console.log('bbb', data)
                const lst = Object.entries(data).map(([key, value])=>{
                    return ({'nickname': key, 'username': value["friend_username"]})
                })
                // console.log(lst)
                setFriendData(lst)
            }
        ).catch(
            error => {
                // console.log('aaa', error)
            }
        )
    },[])
    function changeIsChat() {
        setIsChat(!isChat)
    }

    function quit() {
        back("/", {replace: true})
    }

    function handleInputChange(e) {
        setInputMessage(e.target.value)
    }

    async function loadPreviousHistory() {
        // TODO
    }


    async function update() {
        const response = await fetch('http://localhost:8080/updateChatHistory')
        const data = await response.json()
        if (data.result.length > 0) {
            setMyChatData(data.result)
        }
    }

    async function sendMessage() {
        if (inputRef.current.input.value !== "") {
            setSendButtonLoading(true)
            const message = inputRef.current.input.value
            await fetch(`http://localhost:8080/sendMessage?message=${message}`)
            setInputMessage("")
            setSendButtonLoading(false)
        } else {
            error("Can not send empty message")
        }
    }


    async function addFriend() {
        const username = addFriendUsernameRef.current.input.value
        const nickname = addFriendNicknameRef.current.input.value
        // console.log(username)
        if (!username || !nickname) {
            error("Please input username and nickname")
            return
        }

        const response = await fetch(`http://localhost:8080/addFriend?usrname=${username}&nickname=${nickname}`)
        const data = await response.json()

        if (data.result) {
            const dic = data.message
            const lst = Object.entries(dic).map(([key, value])=>{
                    return ({'nickname': key, 'username': value["friend_username"]})
                })
            setFriendData(lst)
            success(`${nickname} has added to your friend list`)
        } else {
            error(data.message)
        }
    }


    useEffect(()=>{
        // console.log(currentChattingFriend)
        if (currentChattingFriend !== null) {
            const intervalId = setInterval(()=>{
            update()
            }, 2000)
            return ()=> clearInterval(intervalId)
        }
    },[currentChattingFriend])


    async function onClickSelectFriend(nickname) {
        setCurrentChattingFriend(nickname)
        const response = await fetch(`http://localhost:8080/selectFriend?message=${nickname}`)
        const data = await response.json()
        if (data.result.length === 0) {
            error(data.message)
        } else {
            setMyChatData(data.result)
        }

        if (chatListRef.current) {

            chatListRef.current.scrollTop = chatListRef.current.scrollHeight
        }
    }



    return (
        <div className='webPage'>
            {contextHolder}
            <div className={"logos"}>
                <span>
                    <a href="https://blog.resilientdb.com/2023/12/20/ResChat.html" target="_blank">
                        <Image src={reschatLogo} height={50} preview={false}></Image>
                    </a>
                </span>

                <span style={{marginLeft: 20}}>
                    <a href="https://resilientdb.incubator.apache.org/" target="_blank">
                        <Image src={resdbLogo} height={50} preview={false}></Image>
                    </a>
                </span>
                <span style={{marginLeft: 20}}>
                    <a href="https://cs.ucdavis.edu/" target="_blank">
                        <Image src={ucdavisLogo} style={{marginLeft: 0}} height={45} preview={false}></Image>
                    </a>
                </span>
            </div>
            <div className='chatPage'>
                <div className='leftWrap'>

                    <div className='friendList'>
                        <List
                            dataSource={friendData}
                            renderItem={(item, index) => (
                                <List.Item onClick={() => onClickSelectFriend(item.nickname)} className={currentChattingFriend===item.nickname?'friendSelected':'friendNotSelected'}>
                                        <List.Item.Meta
                                            avatar={<Avatar src={`https://api.dicebear.com/7.x/miniavs/svg?seed=${index}`}/>}
                                            title={item.nickname}
                                            description={item.username}
                                        />
                                    </List.Item>
                                )}
                            />
                        </div>

                        <div className='buttonWrap'>
                            {isChat ? <Button type="primary" onClick={changeIsChat} style={{borderRadius: 15}}>Add Friend</Button> : <Button type="primary" onClick={changeIsChat} style={{borderRadius: 15}}>Back</Button>}
                            <Button type="primary" onClick={quit} style={{borderRadius: 15}}>Quit</Button>
                        </div>

                    </div>
                {isChat ? <div className='rightWrap'>
                    <div className='chatList' ref={chatListRef}>
                        <List
                            header={currentChattingFriend !== null ? <div className='loadMore'><Button>Load History</Button></div> : <div/>}
                            dataSource={myChatData}
                            renderItem={(item, index) => (
                                item[5] === 'RECEIVER' ?
                                    // TODO: 聊天记录方向还是有问题
                                    <List.Item>
                                        <List.Item.Meta
                                            avatar={<Avatar
                                                src={`https://api.dicebear.com/7.x/miniavs/svg?seed=${index}`}/>}
                                            title={item[0]}
                                        />
                                    </List.Item> :
                                    <List.Item>
                                        <div className='senderWrap'>
                                            <div className='senderContent'>
                                                {item[0]}
                                            </div>
                                            <Avatar className='senderAvatar'
                                                    src={`https://api.dicebear.com/7.x/miniavs/svg?seed=John`}/>
                                        </div>
                                    </List.Item>
                            )}
                        />
                    </div>
                    <div className='inputWrap'>
                        <Input ref={inputRef} style={{marginLeft: 15, marginRight: 15, borderRadius: 15}} onChange={handleInputChange} value={inputMessage} placeholder="Enter your message"/>
                        <Button onClick={sendMessage} loading={sendButtonLoading} style={{marginRight: 15, borderRadius: 15}} type="primary">Send</Button>

                    </div>
                </div> : <div className='addFriendWrap'>
                    <Input placeholder={"Username"} ref={addFriendUsernameRef} style={{marginTop: '10%', marginLeft: '10%', marginRight: '10%', width: '50%', height: '10%', borderRadius: 15}}/>
                    <Input placeholder={"Nickname"} ref={addFriendNicknameRef} style={{marginTop: '10%', marginLeft: '10%', marginRight: '10%', width: '50%', height: '10%', borderRadius: 15}}/>
                    <Button type="primary" onClick={addFriend} style={{marginTop: '10%', borderRadius: 15, width: '10%', height: '6%'}}> Add </Button>
                </div>}


            </div>
        </div>
    );
}

export default Chat;
