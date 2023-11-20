<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Http\Requests\RatingRequest;
use App\Http\Resources\RatingResource;
use App\Models\Rating;
use App\Models\User;
use App\Models\Shop;

class RatingController extends Controller
{
    public function get($user_id)
    {
        $userRatings = Rating::where('user_id', $user_id)->get();

        
        if ($userRatings == null) {
            return null;
        }


        return RatingResource::collection($userRatings);
    }

    public function post($user_id, RatingRequest $request)
    {
        $user = User::findOrFail($user_id);
        $ratingData = $request->validated();
        $rating = $user->ratings()->create($ratingData);

        return RatingResource::make($rating);
    }

    public function delete($user_id, $shop_id)
    {
        $user = User::findOrFail($user_id);

        // ユーザが評価した店データを削除
        $user->ratings()->where('shop_id', $shop_id)->delete();

        return response()->noContent(); 
    }
}
