import React, { useState, useEffect } from 'react'

import { withStyles, makeStyles } from '@material-ui/core/styles';

import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';

import Button from '@material-ui/core/Button';

import api from "../lib/api.js"

const useStyles = makeStyles((theme) => ({
  table: {
    minWidth: 700,
  },
  root: {
      ...theme.typography.button,
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


const ReservedTripRow = (props) => {
    const {trip, tokenType, accessToken, getTripsInfo, onGetPassengerPath} = props

    const {trip_id, driver_name, departure, destination, payment, available_seats} = trip

    const onDeleteTrip = async() => {
      const apijson = await api({
        cmd: `passenger/trip/${trip_id}`,
        method: 'DELETE',
        header: {
            "accept": "application/json",
            "Authorization": `${tokenType} ${accessToken}`
        },
        data: {
          trip_id:trip_id
        }
      })
      if (apijson.ok) {
          alert("成功刪除")
          getTripsInfo()
          onGetPassengerPath()
      }else{
          alert(`RTripRow.jsx DEL driver/trip/id ${apijson.body.detail}`)
      }
    }

    const onGetDriverPos = async() => {
      const apijson = await api({
        cmd: `passenger/trip/position`,
        method: 'GET',
        header: {
            "accept": "application/json",
            "Authorization": `${tokenType} ${accessToken}`
        },
        data: {
          trip_id:trip_id
        }
      })
      if (apijson.ok) {
          let res = apijson.body.position
          if(res == ''){
            alert("司機尚未發車")
          }else{
            alert(`司機已到 ${res}`)
          }
      }else{
          alert(`RTripRow.jsx GET passenger/trip/position ${apijson.body.detail}`)
      }
    }

    return(
          <React.Fragment>
              <StyledTableRow >
              <StyledTableCell  align="right">{driver_name}</StyledTableCell>
              <StyledTableCell align="right">{departure.location}</StyledTableCell>
              <StyledTableCell align="right">{departure.time}</StyledTableCell>
              <StyledTableCell align="right">{destination.location}</StyledTableCell>
              <StyledTableCell align="right">{destination.time}</StyledTableCell>
              <StyledTableCell align="right">{available_seats}</StyledTableCell>
              <StyledTableCell align="right">{payment}</StyledTableCell>
              <StyledTableCell align="right">
                  <Button color="primary" onClick={e => onGetDriverPos()}>Check Driver Position</Button>
              </StyledTableCell>
              <StyledTableCell>
                  <Button color="secondary" onClick={e => onDeleteTrip()}>DELETE</Button>
              </StyledTableCell>
              </StyledTableRow>
          </React.Fragment>
      )
}

export default ReservedTripRow;