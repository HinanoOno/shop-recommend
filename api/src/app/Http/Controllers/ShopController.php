<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Http\Requests\ShopRequest;
use App\Http\Resources\ShopResource;
use App\Models\Rating;
use App\Models\User;
use App\Models\Shop;

class ShopController extends Controller
{
    public function post(ShopRequest $request)
    {
        $shopData = $request->validated();
        $shop = Shop::create($shopData);
        return ShopResource::make($shop);
    }
    public function get($shop_id)
    {
        if (is_numeric($shop_id)) {
            $shopData = Shop::where('id', $shop_id)->first();
        } else {
            $shopData = Shop::where('shop_id', $shop_id)->first();
        }
    

        if ($shopData == null) {
            //return response()->json(['message' => 'Shop not found']);
            return null;
        }

        return ShopResource::make($shopData);
    }
   
}
