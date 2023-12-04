import React, { useState, useEffect } from "react";
import Header from "../components/header";
import { useAuth } from "../components/authContext";
import { Shop, ShopSearch } from "../api/@types";
import { apiClient } from "../utils/client";

const Python = () => {
  const [data, setData] = useState<ShopSearch[]>([]);
  const [keyword, setKeyword] = useState("");
  const [ratings, setRatings] = useState<{ [shopId: string]: number }>({});

  const auth = useAuth();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await apiClient.python.$get();
        console.log(response);
        setData(response);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  const onClick = async () => {
    console.log(keyword);
    await apiClient.python
      .$post({
        body: { keyword: keyword },
      })
      .then((res) => {
        console.log(res);
        setData(res);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const handleRatingChange = async (shop: ShopSearch, rating: number) => {
    try {
      setRatings((prevRatings) => ({
        ...prevRatings,
        [shop.id]: rating,
      }));

      const existingShop = await apiClient.shop._shop_id(shop.id).$get();

      let newShop: Shop;

      // 戻り値がnullならば
      if (!existingShop) {
        newShop = await apiClient.shop.$post({
          body: {
            shop_id: shop.id,
            name: shop.name,
            address: shop.address,
            logo_image: shop.logo_image,
            genre: shop.genre,
            url: shop.url,
            photo: {
              l: shop.photo?.l,
              m: shop.photo?.m,
              s: shop.photo?.s,
            },
          },
        });
      } else {
        newShop = existingShop;
      }

      if (auth?.user) {
        const requestBody = {
          user_id: auth.user.id,
          shop_id: newShop.id,
          rating: rating,
        };
        const prevRatings = await apiClient.users
          ._user_id(auth.user.id)
          .saved_shops.$get();

        if (prevRatings != null) {
          prevRatings.map(async (rating) => {
            if (rating.shop_id == newShop.id) {
              await apiClient.users
                ._user_id(5)
                .saved_shops._shop_id(newShop.id)
                .$delete();
            }
          });
        }

        apiClient.users
          ._user_id(auth.user.id)
          .saved_shops.$post({ body: requestBody })
          .then((response) => {
            console.log("Rating saved successfully:", response);
          })
          .catch((error) => {
            console.error("Error saving rating:", error);
          });
      }
    } catch (error) {
      console.error("An error occurred:", error);
    }
  };
  console.log(ratings);

  return (
    <>
      <Header user={auth?.user?.name} />
      <div>
        <h1>Python API Data</h1>
        <label>
          Enter Keyword:
          <input
            type="text"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
          />
          <input type="button" value="送信" onClick={onClick} />
        </label>

        <ul>
          {data.map((shop, index) => (
            <div key={shop.id}>
              <h3>{shop.name}</h3>
              <p>{shop.address}</p>
              <img
                src={shop.logo_image?.toString()}
                alt={`Logo for ${shop.name}`}
              />
              <p>Genre: {shop.genre}</p>
              <a
                href={shop.url?.toString()}
                target="_blank"
                rel="noopener noreferrer"
              >
                Visit Website
              </a>
              <div>
                <p>Photos:</p>
                <img src={shop.photo?.l} alt={`Large Photo for ${shop.name}`} />
              </div>
              <div>
                <p>Rate this shop:</p>
                {[1, 2, 3, 4, 5].map((star) => (
                  <span
                    key={star}
                    onClick={() => handleRatingChange(shop, star)}
                    style={{
                      cursor: "pointer",
                      color: star <= ratings[shop.id] ? "gold" : "gray",
                    }}
                  >
                    &#9733;{" "}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </ul>
      </div>
    </>
  );
};

export default Python;
