import React, {Component, useCallback, useEffect, useRef, useState} from 'react';
import { useNavigate, Link } from 'react-router-dom';
import resdbLogo from "./resource/resilientdb_logo.svg";
import ucdavisLogo from "./resource/ucdavis_logo.png";
// import logo from './logo.svg';
import {Avatar, List, Button, Input, Image, message, Space} from 'antd';
import './Chat.css';
import reschatLogo from "./resource/reschat_logo.svg";


function Chat (){
    const[currentChattingFriend, setCurrentChattingFriend] = useState();
    const[myChatData, setMyChatData] = useState([['Hello', 'TEXT', '2024-3-20 23:01', 'NONE', 'RECEIVER'],
        ['HI', 'TEXT', '2024-3-20 23:02', 'NONE', 'SENDER']])
    const [isChat, setIsChat] = useState(true);
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
                console.log('bbb', data)
                const lst = Object.entries(data).map(([key, value])=>{
                    return ({'nickname': key, 'username': value["friend_username"]})
                })
                console.log(lst)
                setFriendData(lst)
            }
        ).catch(
            error => {
                console.log('aaa', error)
            }
        )
    },[])
    function changeIsChat() {
        setIsChat(!isChat)
    }

    function quit() {
        back("/", {replace: true})
    }


    function getChatList() {

    }

    async function sendMessage() {
        const message = inputRef.current.input.value
        await fetch(`http://localhost:8080/sendMessage?message=${message}`)
    }

    async function addFriend() {
        const username = addFriendUsernameRef.current.input.value
        const nickname = addFriendNicknameRef.current.input.value
        console.log(username)
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

    async function selectFriend() {
        //TODO
    }





    useEffect(()=>{
        getChatList()
        console.log(currentChattingFriend)
    },[currentChattingFriend])
    async function onClickSelectFriend(nickname) {
        setCurrentChattingFriend(nickname)
        const response = await fetch(`http://localhost:8080/selectFriend?message=${nickname}`)
        const data = await response.json()
        if (!data.result) {
            error(data.message)
        }
    }



    return (
        <div className='webPage'>
            {contextHolder}
            <div className={"logos"}>
                <a href="https://blog.resilientdb.com/2023/12/20/ResChat.html" target="_blank">
                    <Image src={reschatLogo} width="7%" preview={false}></Image>
                </a>
                <a href="https://resilientdb.incubator.apache.org/" target="_blank">
                    <Image src={resdbLogo} style={{marginLeft: "10%", marginRight: "10%"}} width="6%" preview={false}></Image>
                </a>
                <a href="https://cs.ucdavis.edu/" target="_blank">
                    <Image src={ucdavisLogo} style={{marginLeft: "10%"}} width="6%" preview={false}></Image>
                </a>

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
                    <div className='chatList'>
                        <List
                            dataSource={myChatData}
                            renderItem={(item, index) => (
                                item[4] === 'RECEIVER' ?
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
                                                    src={`https://api.dicebear.com/7.x/miniavs/svg?seed=${index}`}/>
                                        </div>
                                    </List.Item>
                            )}
                        />
                    </div>
                    <div className='inputWrap'>

                        <Input ref={inputRef} style={{marginLeft: 15, marginRight: 15, borderRadius: 15}} placeholder="Enter your message"/>
                        <Button onClick={sendMessage} style={{marginRight: 15, borderRadius: 15}} type="primary">Send</Button>

                    </div>
                </div> : <div className='addFriendWrap'>
                    {/*TODO: Add Friend*/}
                    <Input placeholder={"Username"} ref={addFriendUsernameRef} style={{marginTop: '10%', marginLeft: '10%', marginRight: '10%', width: '50%', height: '10%', borderRadius: 15}}/>
                    <Input placeholder={"Nickname"} ref={addFriendNicknameRef} style={{marginTop: '10%', marginLeft: '10%', marginRight: '10%', width: '50%', height: '10%', borderRadius: 15}}/>
                    <Button type="primary" onClick={addFriend} style={{marginTop: '10%', borderRadius: 15, width: '10%', height: '6%'}}> Add </Button>
                </div>}


            </div>
        </div>
    );
}

export default Chat;
