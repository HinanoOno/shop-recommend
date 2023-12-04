<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Recommendation extends Model
{
    use HasFactory;

    public function user() { 
        
        return $this->belongsTo(\App\Models\User::class);

    }
    
    public function shop() { 
        
        return $this->belongsTo(\App\Models\Rating::class);

    }
    protected $fillable = [
        'user_id',
        'shop_id',
    ];
}
