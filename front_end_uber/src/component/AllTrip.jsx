import React, { useState, useEffect } from 'react'
import { makeStyles, withStyles } from '@material-ui/core/styles';

import Lightbox from './Lightbox';
import TripRow from './TripRow'

import InputLabel from '@material-ui/core/InputLabel';
import FormControl from '@material-ui/core/FormControl';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';

import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

import api from "../lib/api.js"
import { async } from 'regenerator-runtime';

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
    table: {
        minWidth: 700,
      },
}))

const StyledTableCell = withStyles((theme) => ({
    head: {
      backgroundColor: "#777c80",
      color: "white",
    },
    body: {
      fontSize: 14,
    },
  }))(TableCell);
  
const StyledTableRow = withStyles((theme) => ({
    root: {
      '&:nth-of-type(odd)': {
        backgroundColor: theme.palette.action.hover
      },
    },
}))(TableRow);
  

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

const CustomizedTables = (props) => {
    const classes = useStyles();
    const {allTrips,startAddr,dstAddr,tokenType,accessToken } = props
  
    const JoinTrip = async(id, startAddr, dstAddr) => {
        console.log(id, startAddr, dstAddr)

        const apijson = await api({
            cmd: "passenger/trip",
            method: 'POST',
            data:{
                "trip_id": id,
                "departure": startAddr,
                "destination": dstAddr
            } ,
            header: {
                "accept": "*/*",
                "Authorization": `${tokenType} ${accessToken}`,
                "Content-Type": "application/json"
            }
        })

        if (apijson.status == 201) {
            alert("成功加入")
        }else{
            console.log(apijson.body.detail)
            alert(`POST user/login ${apijson.body.detail}`)
        }
    }


    return (
      <TableContainer style={{borderRadius:0}} component={Paper}>
        <Table className={classes.table} aria-label="customized table">
          <TableHead>
            <TableRow>
              <StyledTableCell align="right">Driver</StyledTableCell>
              <StyledTableCell align="right">Departure</StyledTableCell>
              <StyledTableCell align="right">Start Time</StyledTableCell>
              <StyledTableCell align="right">Destination</StyledTableCell>
              <StyledTableCell align="right">Arrival Time</StyledTableCell>
              <StyledTableCell align="right">Available Seats</StyledTableCell>
              <StyledTableCell align="right">Price</StyledTableCell>
              <StyledTableCell align="right"></StyledTableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {allTrips.map((trip,idx) => (
                <StyledTableRow key={idx}>
                    <StyledTableCell  align="right">{trip.driver_name}</StyledTableCell>
                    <StyledTableCell  align="right">{trip.departure.location}</StyledTableCell>
                    <StyledTableCell align="right">{trip.departure.time}</StyledTableCell>
                    <StyledTableCell align="right">{trip.destination.location}</StyledTableCell>
                    <StyledTableCell align="right">{trip.destination.time}</StyledTableCell>
                    <StyledTableCell align="right">{trip.available_seats}</StyledTableCell>
                    <StyledTableCell align="right">{trip.payment}</StyledTableCell>
                    <StyledTableCell align="right">
                        <Button color="primary" onClick={e => JoinTrip(trip.trip_id, startAddr, dstAddr)}>JOIN</Button>
                    </StyledTableCell>
                </StyledTableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    );
  }

const AllTrip = (props) =>{
    const classes = useStyles();

    const {title, coverClick, tokenType, accessToken, loginrole, checkPointList} = props

    const [startAddr, setStartAddr] = useState("");
    const [dstAddr, setDstAddr] = useState("");
    const [scheduled_date, setDate] = useState(GetDate());

    const [allTrips, setAllTrips] = useState([])
    const [isSearched, setSearched] = useState(false)
    const [isZeroTrip, setZeroTrips] = useState(true)

    // useEffect(()=>{
    //     if(checkPointList.length==0) onGetCheckTrip()

    // }, [checkPointList])

    const onSetStartAddr = (addr) => { 
        setStartAddr(addr)
        setSearched(false)
    }
    const onSetDstAddr = (addr) => { 
        setDstAddr(addr)
        setSearched(false)
    }

    const onSubmit = async() => {
        let isStart = false;
        let isDst = false;

        if(startAddr == "" || startAddr == null) alert("請選擇 起點");
        else isStart = true;

        if(dstAddr == "" || dstAddr == null) alert("請選擇 終點");
        else isDst = true;

        if(isStart && isDst){
            let data = {
                departure: startAddr,
                destination: dstAddr,
                boarding_time:scheduled_date,
            }

            const apijson = await api({
                cmd: 'trip',
                method: 'GET',
                header: {
                    "accept": "application/json",
                    "Authorization": `${tokenType} ${accessToken}`
                },
                data:data
            })
            if (apijson.ok) {
                setAllTrips(apijson.body)
                if(apijson.body.length > 0){
                    setZeroTrips(false)
                }else{
                    setZeroTrips(true)
                }
                setSearched(true)
            }else{
                alert(`alltrip.jsx GET trip ${apijson.body.detail}`)
            }
        }
    }


    const ResultRender = () => {
        if(isSearched){
            if(isZeroTrip){
                return(
                     <div style={{ 
                        textAlign: "center",
                        fontWeight: "bold",
                        color: "red"}}>
                                {`${startAddr} -> ${dstAddr} 沒有符合的路線`}
                    </div>)
            }else{
                return(<CustomizedTables startAddr={startAddr} dstAddr={dstAddr} allTrips={allTrips} accessToken={accessToken} tokenType={tokenType}/>)
            }
        }
    }

    return(
        <Lightbox title={title} coverClick={coverClick}>
            <form>
                <div style={{display:"flex", flexDirection:"row", alignItems:"flex-end", justifyContent:"space-between"}}>
                    <div>
                        <div style={{display:"flex", flexDirection:"column", marginTop:"0"}}>
                            <TextField
                                id="datetime-local"
                                label="Boarding Time"
                                type="datetime-local"
                                defaultValue={scheduled_date}
                                className={classes.textField}
                                InputLabelProps={{
                                    shrink: true,
                                }}
                                onChange={ e => setDate(e.target.value)}
                            />
                        </div>
                        <div style={{display:"flex", flexDirection:"column", marginTop:"0"}}>
                            <FormControl className={classes.formControl}>
                                <InputLabel id="demo-simple-start-label">Departure Address</InputLabel>
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
                    </div>
                    <div>
                        <Button
                            className={classes.margin}
                            variant="contained" 
                            color="primary"
                            size = "large"
                            onClick={onSubmit}
                        >
                        Search
                        </Button>
                    </div>
                </div>
            </form>
            {ResultRender()}
        </Lightbox>
    )
}

export default AllTrip;