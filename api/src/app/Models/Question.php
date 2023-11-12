<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use App\Models\Choice;

class Question extends Model
{
    use HasFactory;

    protected $fillable=['content','image','supplement'];

    public function choices(){
        return $this->hasMany(Choice::class);
    }
}
