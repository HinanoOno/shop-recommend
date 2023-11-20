<?php

use App\Http\Controllers\Api\V1\QuestionController;
use App\Http\Controllers\PythonController;
use App\Http\Controllers\RatingController;
use App\Http\Controllers\ShopController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group. Make something great!
|
*/

Route::prefix('v1/admin')->group(function () {
    Route::apiResource('/quizes', QuestionController::class)->parameters(['quizes' => 'quizId']);;
});

Route::prefix('v1')->group(function () {
    Route::apiResource('/python', PythonController::class);
});


Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

/*Route::prefix('v1')->group(function () {
    Route::post('/shops/{shopId}/likes', [LikeController::class, 'likeShop'])
        ->name('likeShop')
        ->where('shopId', '[0-9]+');

    // ショップのいいねを外す
    Route::delete('/shops/{shopId}/likes/{likeId}', [LikeController::class, 'deleteLike'])
        ->name('deleteLike')
        ->where(['shopId' => '[0-9]+', 'likeId' => '[0-9]+']);
});*/

Route::prefix('v1')->group(function () {
    Route::post('/shop', [ShopController::class, 'post'])
    ->name('postShop');
    Route::get('/shop/{shop_id}', [ShopController::class, 'get'])
    ->name('getShop');
    Route::get('/shop_exist/{shop_id}', [ShopController::class, 'check'])
    ->name('checkShop');


    Route::post('/users/{user_id}/saved_shops', [RatingController::class, 'post'])
        ->name('postRate');
    Route::get('/users/{user_id}/saved_shops', [RatingController::class, 'get'])
        ->name('getRate');

    Route::delete('/users/{user_id}/saved_shops/{shop_id}', [RatingController::class, 'delete'])
        ->name('deleteRate');
});
