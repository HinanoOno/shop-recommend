import Axios from 'axios'

const axios2 = Axios.create({
    baseURL: 'http://localhost/',
    headers: {
        'X-Requested-With': 'XMLHttpRequest',
    },
    withCredentials: true,
})


export default axios2