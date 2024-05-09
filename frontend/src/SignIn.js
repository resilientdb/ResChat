import React, {useRef} from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Input, Image, Button, message } from "antd";
import './SignIn.css';
import usernameLogo from "./resource/username_logo.png";
import lockLogo from "./resource/lock_logo.png";
import resdbLogo from "./resource/resilientdb_logo.svg";
import ucdavisLogo from "./resource/ucdavis_logo.png";
import githubLogo from "./resource/github_logo.svg";
import About from "./About";
import reschatLogo from "./resource/reschat_logo.svg"

function SignIn() {
    const [messageApi, contextHolder] = message.useMessage();
    const navigate = useNavigate();
    const usernameRef = useRef(null);
    const passwordRef = useRef(null);
    const error = (text) => {
        messageApi.open({
            type: 'error',
            content: text,
        });
    };
    async function logIn() {
        const username = usernameRef.current.input.value
        const password = passwordRef.current.input.value
        if (!username || !password) {
            error('Please input your username and password')
            return
        }
        const response = await fetch(`http://localhost:8080/login?usrname=${username}&psw=${password}`)
        const data = await response.json()
        if (data.result) {
            navigate("/chat");
        } else {
            error(data.message)
        }

    }

    async function signUp() {
        const username = usernameRef.current.input.value
        const password = passwordRef.current.input.value
        if (!username || !password) {
            error('Please input your username and password')
            return
        }
        const response = await fetch(`http://localhost:8080/signup?usrname=${username}&psw=${password}`)
        const data = await response.json()
        if (data.result) {
            navigate("/chat");
        } else {
            error(data.message);
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
                    <Image src={resdbLogo} style={{marginLeft: "10%", marginRight: "10%"}} width="6%"
                           preview={false}></Image>
                </a>
                <a href="https://cs.ucdavis.edu/" target="_blank">
                    <Image src={ucdavisLogo} style={{marginLeft: "10%"}} width="6%" preview={false}></Image>
                </a>
            </div>
            <div className='logInBox'>
                <div className='welcome'>Welcome to ResChat</div>
                <div className='inputBorder'>
                    <div style={{margin: 5}}><Image src={usernameLogo} width="90%" height="90%" preview={false}/>
                    </div>
                    <Input ref={usernameRef} className="inputBox" placeholder="Username"/>
                </div>
                <div className='inputBorder'>
                    <div style={{margin: 5}}><Image src={lockLogo} width="90%" height="90%" preview={false}></Image>
                    </div>
                    <Input ref={passwordRef} className="inputBox" placeholder="Password"/>
                </div>
                <div className={"buttonBorder"}>
                    <Button onClick={signUp} style={{marginBottom: "5%", width: "40%", height: "20%", borderRadius: 15}}
                            type={"default"}>Sign Up</Button>
                    <Button onClick={logIn} style={{height: "20%", width: "40%", borderRadius: 15}} type={"primary"}>Login</Button>
                </div>
            </div>

        </div>
    );
}

export default SignIn;
