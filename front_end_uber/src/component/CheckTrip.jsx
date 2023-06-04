import React, { useState, useEffect } from 'react'

import Lightbox from './Lightbox';
import TripRow from './TripRow'

import { withStyles, makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

import api from "../lib/api.js"

const useStyles = makeStyles({
  table: {
    minWidth: 700,
  },
});

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


const CustomizedTables = (props) => {
  const classes = useStyles();
  const {trips, tokenType, accessToken, checkPointList, DelTripTrigger, newPathTrigger, setDriving} = props

  return (
    <TableContainer style={{borderRadius:0}} component={Paper}>
      <Table className={classes.table} aria-label="customized table">
        <TableHead>
          <TableRow>
            <StyledTableCell align="right">Start</StyledTableCell>
            <StyledTableCell align="right">Start Time</StyledTableCell>
            <StyledTableCell align="right">Destination</StyledTableCell>
            <StyledTableCell align="right">Arrival Time</StyledTableCell>
            <StyledTableCell align="right">Available Seats</StyledTableCell>
            <StyledTableCell align="right">Price</StyledTableCell>
            <StyledTableCell align="right"></StyledTableCell>
            <StyledTableCell align="right"></StyledTableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {trips.map((trip) => (
            <TripRow 
              key={trip.trip_id} 
              trip={trip} 
              tokenType={tokenType} 
              accessToken={accessToken} 
              checkPointList={checkPointList} 
              DelTripTrigger={DelTripTrigger} 
              newPathTrigger={newPathTrigger}
              setDriving={setDriving}/>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}


const CheckTrip = (props) =>{
    const {title, coverClick, tokenType, accessToken, checkPointList, newPathTrigger} = props
    const [trips, setTrips] = useState([])
    const [driving, setDriving] = useState(false)

    useEffect(()=>{
      getTripsInfo()
    }, [trips.length])

    const DelTripTrigger = () =>{
      getTripsInfo()
    }

    const getTripsInfo = async() => {
      const apijson = await api({
        cmd: "driver/trip",
        method: 'GET',
        header: {
            "accept": "application/json",
            "Authorization": `${tokenType} ${accessToken}`
        }
      })
      if (apijson.ok) {
        setTrips(apijson.body)
        // console.log(apijson.body)
      }else{
        alert(`checkPath.jsx GET driver/trip ${apijson.body.detail}`)
      }
    }

    return(
        <Lightbox title={title} coverClick={!driving?coverClick:null}>
            <CustomizedTables 
              checkPointList={checkPointList} 
              newPathTrigger={newPathTrigger} 
              trips={trips} 
              tokenType={tokenType} 
              accessToken={accessToken} 
              DelTripTrigger={DelTripTrigger}
              setDriving={setDriving}/>
        </Lightbox>
    )
}

export default CheckTrip;