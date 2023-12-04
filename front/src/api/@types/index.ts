/* eslint-disable */
export type Quiz = {
  content: string
  image?: string | undefined
  supplement?: string | undefined
  choices?: Choice[] | undefined
}

export type Choice = {
  question_id: number
  name: string
  valid: boolean
}

export type Keyword = {
  keyword: string
}

export type ShopInput = {
  shop_id: string
  name: string
  address?: string | undefined
  logo_image?: string | undefined
  genre?: string | undefined
  url?: string | undefined

  photo?: {
    l?: string | undefined
    m?: string | undefined
    s?: string | undefined
  } | undefined
}

export type ShopSearch = {
  id: string
  name: string
  address?: string | undefined
  logo_image?: string | undefined
  genre?: string | undefined
  url?: string | undefined

  photo?: {
    l?: string | undefined
    m?: string | undefined
    s?: string | undefined
  } | undefined
}

export type Shop = {
  id: number
  shop_id: string
  name: string
  address?: string | undefined
  logo_image?: string | undefined
  genre?: string | undefined
  url?: string | undefined

  photo?: {
    l?: string | undefined
    m?: string | undefined
    s?: string | undefined
  } | undefined
}

export type User = {
  id: number
  name: string
  email: string
  password: string
}

export type Like = {
  id: number
  userId: number
  shopId: string
}

export type UserShopRating = {
  id: number
  user_id: number
  shop_id: number
  rating: number
}

export type UserShopsRating = UserShopRating[]

export type QuizResponse = Quiz

export type QuizesResponse = Quiz[]

export type ShopResponse = Shop

export type ShopsResponse = Shop[]

export type ShopsSearchResponse = ShopSearch[]

export type ShopsRecommendResponse = number[]

export type UserResponse = User

export type LikeResponse = Like

export type UserShopRatingResponse = UserShopRating

export type UserShopsRatingResponse = UserShopsRating
