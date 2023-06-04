import React, { Component, useState} from 'react'
import {useNavigate} from 'react-router-dom'

import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button'
import TextField from '@material-ui/core/TextField';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import AccountCircle from '@material-ui/icons/AccountCircle';
import VpnKeyIcon from '@mui/icons-material/VpnKey';
import {FaCar} from "react-icons/fa"
import {BsPersonVcard, BsTelephoneFill} from "react-icons/bs"

import api from "../lib/api.js"

const useCssStyles = makeStyles((theme) => ({
  root: {
    minWidth: 500,
    height: "100%",
    width: "50%",
    margin: "auto",
  },
  content: {
    marginTop: "10%"
  },
  title: {
    fontSize: 14,
  },
  pos: {
    marginBottom: 12,
  },
  margin: {
    margin: theme.spacing(1),
  },
}));

const useStyles = makeStyles((theme) => ({
    root: {
      '& > *': {
        margin: theme.spacing(1),
        width: '30ch',
      },
    },
}));

function SimpleCard() {
  const classes = useCssStyles();

  return (
    <Card className={classes.root}>
      <CardContent className={classes.content}>
        <BasicTextFields/>
      </CardContent>
    </Card>
  );
}

function InputWithIcon({children,type, iwi_id, iwi_label, onChangeText}) {
    const classes = useCssStyles();
  
    return (
      <div>
        <div className={classes.margin}>
          <Grid container spacing={1} alignItems="flex-end">
            <Grid item>
              {children}
            </Grid>
            <Grid item>
              <TextField id={iwi_id} required={true} type={type} label={iwi_label} onChange={e => onChangeText(e.target.value)}/>
            </Grid>
          </Grid>
        </div>
      </div>
    );
  }
  
function BasicTextFields(props) {
    const classes = useStyles();
    const [userName, setUserName] = useState("");
    const [realName, setRealName] = useState("");
    const [phone, setPhone] = useState("");
    const [pwd, setPwd] = useState("");
    const [car, setCarType] = useState("");

    const navigate = useNavigate();

    const onSignUp = async() => {
        let isUsername = false;
        let isRealname = false;
        let isPhone = false;
        let isPwd = false;
        let isCar = false;

        if(userName == "" || userName == null) alert("忘了填 Username");
        else isUsername = true;

        if(realName == "" || realName == null) alert("忘了填 Realname");
        else isRealname = true;

        if(phone == "" || phone == null) alert("忘了填 Phone");
        else isPhone = true;

        if(car == "" || car == null) alert("忘了填 CarType");
        else isCar = true;

        if(pwd == "" || pwd == null) alert("忘了填 Password");
        else isPwd = true;

        if(isUsername && isRealname && isPhone && isPwd && isCar){
          const apijson = await api({
              cmd: "user",
              method: 'POST',
              header: {
                  "accept": "*/*",
                  "Content-Type": "application/json"
              },
              data: {
                  "username": userName,
                  "realname": realName,
                  "phone": phone,
                  "car": car,
                  "password": pwd,
                  "user_id": 0
              }
          })
          if (apijson.status == 201) {
              alert("Success to Sign Up")
              navigate("/login")
          }else{
              console.log(apijson)
              alert(`POST user ${apijson.body.detail.msg}`)
          }
        }
    }
    
    return (
        <form 
            className={classes.root} 
            noValidate
            autoComplete="off">
        <div><h2>SIGN UP</h2></div>
        <InputWithIcon 
            iwi_id="userName" 
            iwi_label="userName" 
            onChangeText = {setUserName}
            children={<AccountCircle />}/>
        <InputWithIcon 
            iwi_id="realName" 
            iwi_label="realName" 
            onChangeText = {setRealName}
            children={<BsPersonVcard />}/>
        <InputWithIcon 
            iwi_id="Phone" 
            iwi_label="Phone" 
            onChangeText = {setPhone}
            children={<BsTelephoneFill />}/>
        <InputWithIcon 
            iwi_id="Car Type" 
            iwi_label="Car Type" 
            onChangeText = {setCarType}
            children={<FaCar />}/>

        <InputWithIcon 
            iwi_id="Password" 
            iwi_label="password" 
            type="password"
            onChangeText = {setPwd}
            children={<VpnKeyIcon />}/>
        <div>
            <Button
                variant="contained" 
                color="primary"
                size = "large"
                style={{width:"100%"}}
                onClick={() => onSignUp()}>
                SIGN UP
            </Button>
        </div>
        </form>
    );
}

const Signup = () => {
    return (
        <div className="signuppage">
            <SimpleCard></SimpleCard>
        </div>
    )
}

export default Signup;