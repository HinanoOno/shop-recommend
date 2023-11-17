<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Shop extends Model
{
    use HasFactory;

    public function ratings() { 

        return $this->hasMany(\App\Models\Rating::class);

    }

    protected $fillable = [
        'shop_id', 'name', 'address', 'logo_image', 'genre', 'url', 'photo'
    ];

    // $castsプロパティを使用してJSON形式のフィールドをキャストします。
    /*protected $casts = [
        'photo' => 'array', // 'array' に変更
    ];*/
}
