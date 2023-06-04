import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

import GoogleMap from "./GoogleMap"
import ReservedTrip from './ReservedTrip'
import CheckTrip from './CheckTrip'
import UserData from './UserData'
import AllTrip from './AllTrip'

import { alpha, makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import IconButton from '@material-ui/core/IconButton';
import Typography from '@material-ui/core/Typography';
import Badge from '@material-ui/core/Badge';
import SearchIcon from '@material-ui/icons/Search';
import AccountCircle from '@material-ui/icons/AccountCircle';
import MapIcon from '@mui/icons-material/Map';
import {BiDoorOpen} from "react-icons/bi"

import {FaEnvelopeOpen} from "react-icons/fa"

import api from "../lib/api.js"

const useStyles = makeStyles((theme) => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  },
  grow: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    display: 'none',
    [theme.breakpoints.up('sm')]: {
      display: 'block',
    },
  },
  search: {
    position: 'relative',
    borderRadius: theme.shape.borderRadius,
    backgroundColor: alpha(theme.palette.common.white, 0.15),
    '&:hover': {
      backgroundColor: alpha(theme.palette.common.white, 0.25),
    },
    marginRight: theme.spacing(2),
    marginLeft: 0,
    width: '100%',
    [theme.breakpoints.up('sm')]: {
      marginLeft: theme.spacing(3),
      width: 'auto',
    },
  },
  searchIcon: {
    padding: theme.spacing(0, 2),
    height: '100%',
    position: 'absolute',
    pointerEvents: 'none',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  inputRoot: {
    color: 'inherit',
  },
  inputInput: {
    padding: theme.spacing(1, 1, 1, 0),
    // vertical padding + font size from searchIcon
    paddingLeft: `calc(1em + ${theme.spacing(4)}px)`,
    transition: theme.transitions.create('width'),
    width: '100%',
    [theme.breakpoints.up('md')]: {
      width: '20ch',
    },
  },
  sectionDesktop: {
    display: 'none',
    [theme.breakpoints.up('md')]: {
      display: 'flex',
    },
  },
  sectionMobile: {
    display: 'flex',
    [theme.breakpoints.up('md')]: {
      display: 'none',
    },
  },
  margin: {
    margin: theme.spacing(1),
  },
  textField: {
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
    width: 200,
  },
  svg: {
    "& > span": {
      fontSize: "18px"
    },
    "&:hover": {
      color: "white"
    }
  }
}));

function PrimarySearchAppBar(props) {
  const classes = useStyles();

  return (
    <div className={classes.grow}>
      <AppBar position="static">
        <Toolbar>
          <Typography className={classes.title} variant="h6" noWrap>
            I'm UBER
          </Typography>
          <IconButton className={classes.svg} onClick={props.onClickGetUserData}>
              <AccountCircle className={classes.margin}/> 個人資料
          </IconButton>
          <div className={classes.grow} />
          <div className={classes.sectionDesktop}>
            <IconButton className={classes.svg} onClick={props.onClickAllTrip}>
                <SearchIcon className={classes.margin}/> 搜尋路線
            </IconButton>
            <IconButton className={classes.svg} onClick={props.onClickReserved}>
              <Badge badgeContent={props.paths} color="secondary" overlap="rectangular">
                <FaEnvelopeOpen className={classes.margin}/>
              </Badge>
              已預定路線
            </IconButton>
            <IconButton>
              <AccountCircle />PASSENGER
            </IconButton>
            <IconButton className={classes.svg} onClick={props.onLogout}>
              <BiDoorOpen className={classes.margin}/> 登出
            </IconButton>
          </div>
        </Toolbar>
      </AppBar>
    </div>
  );
}

const Passenger = (props) => {
  const classes = useStyles();

  const [switchLightbox, setSwitch] = useState(false);
  const [paths, setPaths] = useState(0); 
  const [lightboxContent, setLightboxContent] = useState("")
  const [checkPointList, setCheckPointList] = useState([])

  const {tokenType, accessToken, loginrole, onLogout} = props

  const navigate = useNavigate();

  useEffect (()=>{
      if (!tokenType || !accessToken || !loginrole){
          navigate("/login")
      }
  }, [props])

  useEffect(()=>{
    if(accessToken){
      onGetPassengerPath()
      onGetCheckTrip()
      console.log(`passenger.jsx ${paths}useEff paths`)
    }
  }, [paths])

  const onGetPassengerPath = async() => {
    const apijson = await api({
      cmd: "passenger/trip",
      method: 'GET',
      header: {
          "accept": "application/json",
          "Authorization": `${tokenType} ${accessToken}`
      }
    })
    if (apijson.ok) {
      setPaths(apijson.body.length)
    }else{
      alert(`GET passenger/trip ${apijson.body.detail}`)
    }
  } 

  const onOpenSwitch = (title) =>{ 
    setLightboxContent(title)
    setSwitch(true) 
  }

  const onCloseSwitch = () =>{ 
    setLightboxContent("")
    setSwitch(false) 
  }

  const onClickAllTrip = () => {
    onOpenSwitch("搜尋路線")
  }

  const onClickGetUserData = () =>{
    onOpenSwitch("個人資料")
  }

  const onClickReserved = () => {
    onOpenSwitch("已預定路線")
  }

  const onGetCheckTrip = async() => {
    const apijson = await api({
        cmd: 'trip/maps',
        method: 'GET',
        header: {
            "accept": "application/json",
            "Authorization": `${tokenType} ${accessToken}`
        }
      })
    if (apijson.ok) {
        setCheckPointList(apijson.body)
    }else{
        alert(`alltrip.jsx GET trip ${apijson.body.detail}`)
    }
  }

  return (
    <div className="content">
      { lightboxContent == "個人資料" ?
        <UserData 
        title={lightboxContent} tokenType={tokenType} accessToken={accessToken} loginrole={loginrole} coverClick={onCloseSwitch} /> :null}
      { lightboxContent == "搜尋路線" ?
        <AllTrip checkPointList={checkPointList}
        title={lightboxContent} tokenType={tokenType} accessToken={accessToken} loginrole={loginrole} coverClick={onCloseSwitch} /> :null}
      { lightboxContent == "已預定路線" ?
        <ReservedTrip checkPointList={checkPointList} onGetPassengerPath={onGetPassengerPath}
        title={lightboxContent} tokenType={tokenType} accessToken={accessToken} loginrole={loginrole} coverClick={onCloseSwitch} />:null}
      <div className="userPage">
        <PrimarySearchAppBar
          paths = {paths}
          onClickAllTrip = {onClickAllTrip}
          onClickGetUserData = {onClickGetUserData}
          onClickReserved = {onClickReserved}
          onLogout={onLogout}
        />
        <div>
          <GoogleMap/>
          <div></div>
        </div>
      </div>
    </div>
  )
}

export default Passenger;