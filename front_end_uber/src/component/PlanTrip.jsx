import React, { useState, useEffect } from 'react'
import { makeStyles } from '@material-ui/core/styles';

import Lightbox from './Lightbox';
import CheckPointSelect from "./CheckPointSelect"

import InputLabel from '@material-ui/core/InputLabel';
import FormControl from '@material-ui/core/FormControl';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';


import {IoIosPin} from "react-icons/io";
import {AiFillFlag} from "react-icons/ai";
import {GoPlus} from 'react-icons/go';
import {RxCross2} from 'react-icons/rx';
import {MdOutlineChairAlt} from "react-icons/md"

import api from "../lib/api.js"

const useStyles = makeStyles((theme) => ({
    textField: {
        marginLeft: theme.spacing(1),
        marginRight: theme.spacing(1),
        width: 200,
    },
    seattextField: {
        marginLeft: theme.spacing(1),
        marginRight: theme.spacing(1),
        width: 50,
    },
    margin: {
        margin: theme.spacing(1),
    },
    formControl: {
        margin: theme.spacing(1),
        minWidth: 450,
      },
}))

const GetDate = () => {
    let curDate = new Date();
    let month = curDate.getMonth()+1
    let day = curDate.getDate()
    let hour = curDate.getHours()
    let min = curDate.getMinutes()
    if (day < 10) {
        day = '0' + day;
    }

    if (month < 10) {
        month = `0${month}`;
    }

    if (hour < 10) {
        hour = `0${hour}`;
    }

    if (min < 10) {
        min = `0${min}`;
    }

    let curDateFormat = `${curDate.getFullYear()}-${month}-${day}T${hour}:${min}`
    return curDateFormat
}

const PlanTrip = (props) => {
    const classes = useStyles();

    const {coverClick, title, tokenType, accessToken, checkPointList} = props

    // const [checkPointList, setCheckPointList] = useState([])
    const [startAddr, setStartAddr] = useState("");
    const [dstAddr, setDstAddr] = useState("");
    const [scheduled_date, setDate] = useState(GetDate());
    const [numSeat, setNumSeat] = useState(0);
    const [targetList, setTargetList] = useState([]); // 選好的 check point

    const onSetStartAddr = (addr) => { setStartAddr(addr)}
    const onSetDstAddr = (addr) => { setDstAddr(addr)}

    const onRemoveTarget = (idx) => {
        const firstArr = targetList.slice(0, idx);
        const secondArr = targetList.slice(idx + 1);
        setTargetList([...firstArr, ...secondArr])
    }

    const changeTargetList = (idx, value) => {
        let tmp = targetList
        tmp[idx] = value
        setTargetList(tmp)
    }

    const handleChange = (event) => {
        setTargetList([...targetList, event.target.value])
    };

    const onSubmit = async() => {
        let isSeat = false;
        let isStart = false;
        let isDst = false;

        if(startAddr == "" || startAddr == null) alert("請選擇 起點");
        else isStart = true;

        if(dstAddr == "" || dstAddr == null) alert("請選擇 終點");
        else isDst = true;
  
        if(numSeat == 0 || numSeat == null) alert("請選擇 乘客數");
        else isSeat = true;

        if(startAddr && dstAddr && numSeat){
            let data = {
                boarding_time: scheduled_date,
                available_seats: numSeat,
                path:[startAddr, ...targetList, dstAddr],
            }

            
            const apijson = await api({
                cmd: "driver/trip",
                method: 'POST',
                data: data,
                header: {
                    "accept": "*/*",
                    "Content-Type": "application/json",
                    "Authorization": `${tokenType} ${accessToken}`
                }
            })
            if (apijson.status == 201) {
                alert("Success to New Trip ")
            }else{
                alert(`POST driver/trip ${apijson.body.detail}`)
            }

            props.newPathTrigger()
            props.coverClick()
        }
    }

    return(
        <Lightbox title={title} coverClick={coverClick}>
            <form>
                <div style={{display:"flex", flexDirection:"row"}}>
                    <TextField
                        id="datetime-local"
                        label="Next appointment"
                        type="datetime-local"
                        defaultValue={scheduled_date}
                        className={classes.textField}
                        InputLabelProps={{
                            shrink: true,
                        }}
                        onChange={ e => setDate(e.target.value)}
                    />
                    <FormControl className={classes.seattextField}>
                        <InputLabel id="demo-simple-seat-label">Seat</InputLabel>
                        <Select
                        labelId="demo-simple-seat-label"
                        id="demo-seat-select"
                        value={numSeat}
                        onChange={e => setNumSeat(e.target.value)}
                        >
                            {[1,2,3,4,5,6].map(d=> {
                                return(
                                    <MenuItem key={d} value={d}>{d}</MenuItem>
                                )
                            })}
                        </Select>
                    </FormControl>
                </div>
                <div style={{display:"flex", flexDirection:"column", marginTop:"0"}}>
                    <FormControl className={classes.formControl}>
                        <InputLabel id="demo-simple-start-label">Start Address</InputLabel>
                        <Select
                        labelId="demo-simple-start-label"
                        id="demo-simple-start"
                        value={startAddr}
                        onChange={e => onSetStartAddr(e.target.value)}
                        >
                            {checkPointList && checkPointList.map((cp, idx)=> {
                                return(
                                    <MenuItem key={idx} value={cp.location}>{cp.location}</MenuItem>
                                )
                            })}
                        </Select>
                    </FormControl>
                </div>
                <div style={{display:"flex",alignItems:"flex-end"}}>
                    <div style={{display:"flex", flexDirection:"column"}}>
                        {
                        targetList && targetList.map((t, id)=>{
                            return(
                                <div key={id} style={{display:"flex", flexDirection:"row", marginTop:"0", alignItems:"flex-end"}}>
                                    <CheckPointSelect id={id} value={t} checkPointList={checkPointList} changeTargetList={changeTargetList}></CheckPointSelect>
                                    <RxCross2  className={classes.margin} color="#FF5733" onClick={()=>onRemoveTarget(id)}/>
                                </div>
                                )
                            })
                        }
                        <div style={{display:"flex", flexDirection:"row", marginTop:"0", alignItems:"flex-end"}}>
                            <div style={{display:"flex", flexDirection:"row", alignItems: "flex-end"}}>
                                <FormControl className={classes.formControl}>
                                    <InputLabel id="demo-simple-select-label">Check Point</InputLabel>
                                    <Select
                                    labelId="demo-simple-select-label"
                                    id="demo-simple-select"
                                    value={""}
                                    onChange={handleChange}
                                    >
                                        {checkPointList && checkPointList.map((cp, idx)=> {
                                            return(
                                                <MenuItem key={idx} value={cp.location}>{cp.location}</MenuItem>
                                            )
                                        })}
                                    </Select>
                                </FormControl>
                            </div>
                            {/* <RxCross2  className={classes.margin} color="#FF5733"/> */}
                        </div>
                    </div>
                </div>

                <div style={{display:"flex", flexDirection:"column", marginTop:"0"}}>
                    <FormControl className={classes.formControl}>
                        <InputLabel id="demo-simple-dst-label">Destination Address</InputLabel>
                        <Select
                        labelId="demo-simple-dst-label"
                        id="demo-dst-start"
                        value={dstAddr}
                        onChange={e => onSetDstAddr(e.target.value)}
                        >
                            {checkPointList && checkPointList.map((cp, idx)=> {
                                return(
                                    <MenuItem key={idx} value={cp.location}>{cp.location}</MenuItem>
                                )
                            })}
                        </Select>
                    </FormControl>
                </div>
                <Button
                    className={classes.margin}
                    variant="contained" 
                    color="primary"
                    size = "large"
                    onClick={onSubmit}
                >
                Go
                </Button>
            </form>
        </Lightbox>
    )
}

export default PlanTrip;