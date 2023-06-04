import React, { useState, useEffect } from 'react'
import { makeStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 450,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  },
}));

const CheckPointSelect = (props) => {
    const classes = useStyles();
    const { checkPointList } = props

    const [targetCheckPoint, setTargetCheckPoint] = useState("")

    useEffect(() => {
        setTargetCheckPoint(props.value)
    }, [props.value])

    const handleChange = (event) => {
        setTargetCheckPoint(event.target.value);
    };

  return (
    <div style={{display:"flex", flexDirection:"row", alignItems: "flex-end"}}>
        <FormControl className={classes.formControl}>
            <InputLabel id="demo-simple-select-label">Check Point</InputLabel>
            <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={targetCheckPoint}
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
  );
}

export default CheckPointSelect;