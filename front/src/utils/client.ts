import aspida from '@aspida/axios'
import api from '../api/$api'
import axios from '../lib/axios';

export const apiClient = api(aspida(axios));