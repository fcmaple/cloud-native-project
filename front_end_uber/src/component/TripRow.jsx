import React, { useEffect, useState } from 'react'

import { withStyles, makeStyles } from '@material-ui/core/styles';

import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';

import Button from '@material-ui/core/Button';

import {IoIosPin} from "react-icons/io";
import {AiFillFlag} from "react-icons/ai";
import {BiUpArrowCircle,BiDownArrowCircle} from "react-icons/bi"

import api from "../lib/api.js"
import { async } from 'regenerator-runtime';

const useStyles = makeStyles((theme) => ({
    table: {
      minWidth: 700,
    },
    root: {
        ...theme.typography.button,
        position: "relative",
        backgroundColor: theme.palette.background.paper,
        padding: theme.spacing(1),
        display: "flex",
        alignItems: "center",
        fontSize: 20
    },
    svg: {
        cursor:"default",
        marginLeft:"5px",
        padding:"5px", 
        height:"25", 
        width:"25"
    },
    btn: {
        position: "absolute",
        right: "0"
    }
}));

const StyledTableCell = withStyles((theme) => ({
    head: {
      backgroundColor: "#777c80",
      color: "white",
    },
    body: {
      fontSize: 16,
      padding: 10
    },
  }))(TableCell);

const StyledTableRow = withStyles((theme) => ({
    root: {
      '&:nth-of-type(odd)': {
        backgroundColor: theme.palette.action.hover
      },
    },
}))(TableRow);


const TripDetail = (props) =>{
    const classes = useStyles();

    const {tripDetail, StartTrip, postionIdx, updateTrip, setPosIdx, starting, doneTrip} = props
    let startInfo = tripDetail[0]
    let dstInfo = tripDetail[tripDetail.length-1]
    let checkpointInfo = tripDetail.slice(1, tripDetail.length-1)


    const clickhandler = (location, idx) =>{
        updateTrip(location)
        setPosIdx(idx+1)
        if(idx == tripDetail.length-1) {
            doneTrip()
        }
    }
    return(
        <div>
            <div className={classes.root}>
                <IoIosPin className={classes.svg} color="#FF5733"/>
                    {`${startInfo.point.location}  ${startInfo.point.time} `}
                <BiUpArrowCircle className={classes.svg}color="gray"/>
                    {startInfo.boarding}
                <BiDownArrowCircle className={classes.svg} color="gray"/>
                    {startInfo.Alighting}
                {
                    starting && postionIdx == 0 
                    ?<Button
                        className={classes.btn}
                        variant="contained" 
                        color="primary"
                        size = "large"
                        onClick={() => clickhandler(startInfo.point.location, 0)}>
                        抵達
                    </Button>
                    :null
                }
            </div>
            {
                checkpointInfo.length > 0 && checkpointInfo.map((cp, idx) => {
                    return(
                        <div className={classes.root} key={idx}>
                            <AiFillFlag className={classes.svg} color="gray"/>
                                {`${cp.point.location}  ${cp.point.time} `}
                            <BiUpArrowCircle className={classes.svg}color="gray"/>
                                {cp.boarding}
                            <BiDownArrowCircle className={classes.svg} color="gray"/>
                                {cp.Alighting}
                                {
                                    starting && postionIdx == idx+1
                                    ?<Button
                                        className={classes.btn}
                                        variant="contained" 
                                        color="primary"
                                        size = "large"
                                        onClick={() => clickhandler(cp.point.location, idx+1)}>
                                        抵達
                                    </Button>
                                    :null
                                }
                        </div>
                    )
                })
            }
           
            <div className={classes.root}>
                <AiFillFlag className={classes.svg} color="#FF5733"/>
                    {`${dstInfo.point.location}  ${dstInfo.point.time} `}
                <BiUpArrowCircle className={classes.svg}color="gray"/>
                    {dstInfo.boarding}
                <BiDownArrowCircle className={classes.svg} color="gray"/>
                    {dstInfo.Alighting}
                    {
                        starting && postionIdx == tripDetail.length-1
                        ?<Button
                            className={classes.btn}
                            variant="contained" 
                            color="primary"
                            size = "large"
                            onClick={() => clickhandler(dstInfo.point.location, tripDetail.length-1)}>
                            抵達
                        </Button>
                        :null
                    }
            </div>
            <div className={classes.root}>
                {!starting
                ?<Button
                    variant="contained" 
                    color="primary"
                    size = "large"
                    onClick={() => StartTrip()}>
                    START
                </Button>
                :<Button 
                    disabled
                    variant="contained"
                    size = "large">
                    行駛中
                </Button>
                }
            </div>
        </div>
    )
}

const TripRow = (props) => {
    const {trip, tokenType, accessToken, checkPointList, DelTripTrigger, newPathTrigger, setDriving} = props

    const classes = useStyles();

    const [tripDetail, setTripDetail] = useState([])
    const [showDetail, setShow] = useState(false)
    const [starting, setStarting] = useState(false)
    const [postionIdx, setPosIdx] = useState(0)

    let start = trip.departure
    let dst = trip.destination

    const doneTrip = async() => {
        const apijson = await api({
            cmd: `driver/trip/${trip.trip_id}`,
            method: 'DELETE',
            header: {
                "accept": "application/json",
                "Authorization": `${tokenType} ${accessToken}`
            },
            data: {
                trip_id:trip.trip_id
            }
        })
        if (apijson.ok) {
            DelTripTrigger()
            newPathTrigger()
            setDriving(false)
            alert("已成功完成")
        }else{
            alert(`checkPath.jsx DEL driver/trip/id ${apijson.body.detail}`)
        }
    }

    const onDeleteTrip = async() => {
        const apijson = await api({
          cmd: `driver/trip/${trip.trip_id}`,
          method: 'DELETE',
          header: {
              "accept": "application/json",
              "Authorization": `${tokenType} ${accessToken}`
          },
          data: {
            trip_id:trip.trip_id
          }
        })
        if (apijson.ok) {
            DelTripTrigger()
            newPathTrigger()
            setDriving(false)
            alert("成功刪除")
        }else{
            alert(`checkPath.jsx DEL driver/trip/id ${apijson.body.detail}`)
        }
    }
  
    const updateTrip = async(location) => {
        const apijson = await api({
            cmd: `driver/trip/position`,
            method: 'PUT',
            header: {
              "accept": "application/json",
              "Authorization": `${tokenType} ${accessToken}`
            },
            data: {
              "trip_id":trip.trip_id,
              "position": location
            }
          })
          if (apijson.ok) {
            //   console.log(apijson.body)
          }else{
              console.log(`TripRow.jsx PUT driver/trip/id ${apijson.body}`)
          }
    }

    const onGetTripInfo = async() =>{
        const apijson = await api({
          cmd: `driver/trip/${trip.trip_id}`,
          method: 'GET',
          header: {
            "accept": "application/json",
            "Authorization": `${tokenType} ${accessToken}`
          },
          data: {
            "trip_id":trip.trip_id
          }
        })
        if (apijson.ok) {
            setTripDetail(apijson.body)
            console.log(apijson.body)
        }else{
            alert(`checkPath.jsx GET driver/trip/id ${apijson.body.detail}`)
        }

        setShow(true)
    }

    const StartTrip = () => {
        setDriving(true)
        setStarting(true)
        setPosIdx(0)
    }

    return(
    // <StyledTableRow key={trip.trip_id}>
        <React.Fragment>
            <StyledTableRow >
            <StyledTableCell  align="right">{start.location}</StyledTableCell>
            <StyledTableCell align="right">{start.time}</StyledTableCell>
            <StyledTableCell align="right">{dst.location}</StyledTableCell>
            <StyledTableCell align="right">{dst.time}</StyledTableCell>
            <StyledTableCell align="right">{trip.available_seats}</StyledTableCell>
            <StyledTableCell align="right">{0}</StyledTableCell>
            <StyledTableCell align="right">
                {!showDetail && <Button color="primary" onClick={e => onGetTripInfo()}>MORE...</Button>}
            </StyledTableCell>
            <StyledTableCell>
                <Button color="secondary" onClick={e => onDeleteTrip()}>DELETE</Button>
            </StyledTableCell>
            </StyledTableRow>
            {showDetail && 
                <StyledTableRow>
                <StyledTableCell colSpan="8">
                    <TripDetail 
                        tripDetail={tripDetail} 
                        StartTrip={StartTrip} 
                        starting={starting} 
                        postionIdx={postionIdx} 
                        updateTrip={updateTrip} 
                        setPosIdx={setPosIdx}
                        doneTrip={doneTrip}/>
                </StyledTableCell>
                </StyledTableRow>
            }
        </React.Fragment>
    )
}

export default TripRow;