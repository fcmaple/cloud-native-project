import axios from 'axios'
import 'regenerator-runtime/runtime'

// import apiurl from '../../public/config.js'

let apiurl;

axios.get('./config.json').then(res => {
	if (res.status === 200) {
		apiurl = res.data.apiurl
	}
  })


export default function ({
	cmd = '',
	method = 'GET',
	type = 'json',
	data = {},
	header = {},
	fileList = [],
}) {
	method = method.toUpperCase()
	type = type.toLowerCase()
	let url = `${apiurl}/${cmd}`
	let cors = false
	let option = {
		method,
		headers: {
			'Content-Type': 'application/json',
			...header,
		}
	}
	switch (method) {
		case 'POST':
		case 'DELETE':
			option.data = data
			break;
		case 'PUT':
		case 'GET':
			option.params = data
			break;
	}
	return axios({
		method,
		url,
		...option,
		withCredentials: !!cors,
	}).then((res) => {
		return {
			ok: res.statusText == 'OK',
			status: res.status,
			body: res.data
		}
	})
		.catch(err => {
			let res = err.response
			if (res) {
				return {
					ok: res.statusText == 'OK',
					status: res.status,
					body: res.data
				}
			}
			else {
				return {
					ok: false,
					status: "500",
					body: err.message
				}
			}
		})
}