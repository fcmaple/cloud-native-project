import React, {useState} from 'react'
import { makeStyles } from '@material-ui/core/styles';
import { Link } from "react-router-dom";
import {FaCarAlt} from 'react-icons/fa'
import {FaUsers} from 'react-icons/fa'
import Button from '@material-ui/core/Button'
import TextField from '@material-ui/core/TextField';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Grid from '@material-ui/core/Grid';
import AccountCircle from '@material-ui/icons/AccountCircle';
import VpnKeyIcon from '@mui/icons-material/VpnKey';

import api from "../lib/api.js"

const useCaedStyles = makeStyles({
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
});

function SimpleCard(props) {
  const classes = useCaedStyles();
  const {onSubmit, onChangeRole} = props
  return (
    <Card className={classes.root}>
      <CardContent className={classes.content}>
        <BasicTextFields onSubmit={onSubmit} onChangeRole={onChangeRole}/>
      </CardContent>
    </Card>
  );
}

const useInputWithIconStyles = makeStyles((theme) => ({
    margin: {
      margin: theme.spacing(1),
    },
  }));
  
  function InputWithIcon({children, type, iwi_id, iwi_label, onChangeText}) {
    const classes = useInputWithIconStyles();
  
    return (
      <div>
        <div className={classes.margin}>
          <Grid container spacing={1} alignItems="flex-end">
            <Grid item>
              {children}
            </Grid>
            <Grid item>
              <TextField 
                id={iwi_id} 
                type={type} 
                required={true} 
                label={iwi_label} 
                onChange={e => onChangeText(e.target.value)}/>
            </Grid>
          </Grid>
        </div>
      </div>
    );
  }

const useStyles = makeStyles((theme) => ({
    root: {
      '& > *': {
        display: 'flex',
        flexdirection: 'column',
        margin: theme.spacing(1),
        width: '30ch',
      },
    },
  }));

function BasicTextFields(props) {
    const classes = useStyles();
    const [userName, setUserName] = useState("");
    const [pwd, setPwd] = useState("");
    const [role, setRole] = useState("");
    const [svgColor, setSvgColor] = useState("gray")
    const [svgClickedColor, setClickedColor] = useState("black")
    const {onSubmit} = props

    function onChange(type){
        setRole(type)
    }

    const onSubmithandler = () => {
        const form_data = {
            username: userName,
            password: pwd,
            role: role
        }

        onSubmit({...form_data})
    }

    return (
        <form 
            className={classes.root} 
            noValidate
            autoComplete="off">
        <div><h2>LOGIN</h2></div>
        <InputWithIcon 
            iwi_id="Username" 
            iwi_label="Username" 
            onChangeText = {setUserName}
            children={<AccountCircle />}/>
        <InputWithIcon
            iwi_id="Password" 
            iwi_label="password" 
            onChangeText = {setPwd}
            type="password"
            children={<VpnKeyIcon />}/>
        <div className='icon_list'>
            <div className='icon_wrapper'>
                <FaCarAlt 
                    size="50" 
                    color={role=="driver"?svgClickedColor:svgColor}
                    onClick={() => onChange("driver")}/> 
            </div>
            <div className='icon_wrapper'>
                <FaUsers 
                    size="50" 
                    color={role=="passenger"?svgClickedColor:svgColor}
                    onClick={() => onChange("passenger")}/>
            </div>
        </div>
        <div>
            <Button
                variant="contained" 
                color="primary"
                size = "large"
                style={{width:"100%"}}
                onClick={() => onSubmithandler()}>
                LOGIN
            </Button>
        </div>

        <div className="container"><span>Don't have an account?</span><Link to="/signup">Sign Up</Link>
        </div>
        </form>
    );
}

const Login = (props) => {
  const { onChangeRole, getGkey,setIsLogIn} = props

  const onSubmit = async (formdata) => {
      const {onSetAccessToke} = props

      const {username, password, role} = formdata

      let isUsername = false;
      let isPwd = false;
      let isRole = false;

      if(username == "" || username == null) alert("忘了填 Username");
      else isUsername = true;

      if(password == "" || password == null) alert("忘了填 Password");
      else isPwd = true;

      if(role == "" || role == null) alert("忘了選 登入身份");
      else isRole = true;

      
      if(isUsername && isPwd &&  isRole){
        setIsLogIn(true)
        const key= getGkey()
        const apijson = await api({
            cmd: "user/login",
            method: 'POST',
            data:`'grant_type=&username=${username}&password=${password}&scope=&client_id=&client_secret='` ,
            header: {
                "accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded"
            }
        })
        if (apijson.ok) {
            const {access_token, token_type} = apijson.body
            onSetAccessToke({tokenType: token_type,accessToken: access_token, role:role})
        }else{
            alert(`POST user/login ${apijson.body.detail}`)
        }
      }
  }
  return (
      <div className="loginpage" >
          <SimpleCard onSubmit={onSubmit} onChangeRole={onChangeRole}></SimpleCard>
      </div>
  )
}

export default Login;