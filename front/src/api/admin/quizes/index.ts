/* eslint-disable */
import type * as Types from '../../@types'

export type Methods = {
  post: {
    status: 201
    /** 成功 */
    resBody: Types.Quiz[]
    /** 一問クイズ作成 */
    reqBody: Types.Quiz
  }

  get: {
    status: 200
    /** 成功 */
    resBody: Types.Quiz[]
  }
}
