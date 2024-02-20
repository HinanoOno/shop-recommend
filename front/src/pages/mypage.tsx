import React, { useEffect, useState } from "react";
import { useAuth } from "../components/authContext";
import { apiClient } from "../utils/client";
import { UserShopsRatingResponse, Shop } from "../api/@types";
import { set } from "react-hook-form";

type ShopRate = {
  shop: Shop;
  rating: number;
};

const MyPage = () => {
  const auth = useAuth();
  console.log(auth?.user?.name);
  const [shops, setShops] = useState<ShopRate[] | undefined>(undefined);
  const [recommend_shops, setRecommendShops] = useState<{ shop: Shop; }[] | undefined>(undefined);

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (auth?.user) {
          setShops(undefined);
          const response = await apiClient.users._user_id(5).saved_shops.$get();
          console.log(response);
          response.map(async (res, index) => {
            const data = await apiClient.shop._shop_id(res.shop_id).$get();
            setShops((prevData) =>
              prevData
                ? [...prevData, { shop: data, rating: res.rating }]
                : [{ shop: data, rating: res.rating }]
            );
          });
        }
      } catch (error) {
        console.error(error);
      }
    };

    fetchData();
  }, [auth]);

  //おすすめの店取得
  useEffect(() => {
    const recommendData = async () => {
      try {
        if (auth?.user) {
          const responses = await apiClient.python._userId(5).$get();
          console.log(responses);
          const shopDataArray = await Promise.all(
            responses.map(async (response) => {
              const data = await apiClient.shop._shop_id(response).$get();
              return { shop: data };
            })
          );
          setRecommendShops(shopDataArray);
        }
      } catch (error) {
        console.error(error);
      }
    };
    recommendData();
  }, [auth]);


  if (!auth?.user) {
    return <p>ログインしていません。</p>;
  }
  console.log(recommend_shops);

  return (
    <>
      <div>
        <h2>マイページ</h2>
        <p>ユーザーID: {auth.user.id}</p>
        <p>ユーザー名: {auth.user.name}</p>
        <p>Email: {auth.user.email}</p>
      </div>
      <ul>
        <h1>あなたが評価した店一覧</h1>
        {shops &&
          shops.map((shop, index) => (
            <div key={shop.shop.id}>
              <div>
                <h3>{shop.shop.name}</h3>
                <p>{shop.shop.address}</p>
                <img
                  src={shop.shop.logo_image?.toString()}
                  alt={`Logo for ${shop.shop.name}`}
                />
                <p>Genre: {shop.shop.genre}</p>
                <a
                  href={shop.shop.url?.toString()}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Visit Website
                </a>
                <div>
                  <p>Photos:</p>
                  <img
                    src={shop.shop.photo?.l}
                    alt={`Large Photo for ${shop.shop.name}`}
                  />
                </div>
              </div>
              <div>
                <p>あなたの気になる度</p>
                {[1, 2, 3, 4, 5].map((star) => (
                  <span
                    key={star}
                    style={{
                      cursor: "pointer",
                      color: star <= shop.rating ? "gold" : "gray",
                    }}
                  >
                    &#9733;{" "}
                  </span>
                ))}
              </div>
            </div>
          ))}
      </ul>
      <ul>
        <h1>あなたへのおすすめ</h1>
        {recommend_shops &&
          recommend_shops.map((shop, index) => (
            <div key={shop.shop.id}>
              <div>
                <h3>{shop.shop.name}</h3>
                <p>{shop.shop.address}</p>
                <img
                  src={shop.shop.logo_image?.toString()}
                  alt={`Logo for ${shop.shop.name}`}
                />
                <p>Genre: {shop.shop.genre}</p>
                <a
                  href={shop.shop.url?.toString()}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Visit Website
                </a>
                <div>
                  <p>Photos:</p>
                  <img
                    src={shop.shop.photo?.l}
                    alt={`Large Photo for ${shop.shop.name}`}
                  />
                </div>
              </div>
            </div>
          ))}
      </ul>
    </>
  );
};

export default MyPage;
