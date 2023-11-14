<?php

use App\Http\Controllers\Api\V1\QuestionController;
use App\Http\Controllers\PythonController;
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
Route::prefix('v1/admin')->group(function(){
    Route::apiResource('/quizes',QuestionController::class)->parameters(['quizes' => 'quizId']);;
});

Route::prefix('v1')->group(function(){
    Route::apiResource('/python',PythonController::class);
});


Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

