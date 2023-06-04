import React, { useState, useEffect } from 'react'

import Lightbox from './Lightbox';

import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import Avatar from '@material-ui/core/Avatar';

import AccountCircle from '@material-ui/icons/AccountCircle';
import {FaCar} from "react-icons/fa"
import {BsTelephoneFill, BsPersonVcard} from "react-icons/bs"

import api from "../lib/api.js"

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
    maxWidth: 360,
    backgroundColor: theme.palette.background.paper,
  },
}));

const FolderList = (props)=>{
  const {car, phone, realname, username} = props.userData
  const classes = useStyles();

  return (
    <List className={classes.root}>
      <ListItem>
        <ListItemAvatar>
          <Avatar>
            <AccountCircle />
          </Avatar>
        </ListItemAvatar>
        <ListItemText primary="User Name" secondary={username} />
      </ListItem>

      <ListItem>
        <ListItemAvatar>
          <Avatar>
            <BsPersonVcard />
          </Avatar>
        </ListItemAvatar>
        <ListItemText primary="Real Name" secondary={realname} />
      </ListItem>

      <ListItem>
        <ListItemAvatar>
          <Avatar>
            <BsTelephoneFill />
          </Avatar>
        </ListItemAvatar>
        <ListItemText primary="Phone" secondary={phone} />
      </ListItem>

      {car &&
      <ListItem>
        <ListItemAvatar>
          <Avatar>
            <FaCar />
          </Avatar>
        </ListItemAvatar>
        <ListItemText primary="Car" secondary={car} />
        </ListItem>}
    </List>
  );
}


const UserData = (props) => {
    const {tokenType, accessToken, loginrole, title, coverClick} = props
    const [userData, setUserData] = useState({})

    useEffect(() => {
      onGetUserData()
    }, [props])

    const onGetUserData = async() => {
      const apijson = await api({
        cmd: "user",
        method: 'GET',
        header: {
            "accept": "application/json",
            "Authorization": `${tokenType} ${accessToken}`
        }
      })
      if (apijson.ok) {
        setUserData(apijson.body)
      }else{
        alert(`GET user ${apijson.body.detail}`)
      }
    }
    return (
        <Lightbox title={title} coverClick={coverClick}>
            <FolderList userData={userData} />
        </Lightbox>
    )
}

export default UserData;