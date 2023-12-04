/* eslint-disable */
import type * as Types from '../../../@types'

export type Methods = {
  get: {
    status: 200
    /** 成功 */
    resBody: Types.UserShopsRating
  }

  post: {
    status: 201
    /** 成功 */
    resBody: Types.UserShopRating

    reqBody: {
      user_id: number
      shop_id: number
      rating: number
    }
  }
}
