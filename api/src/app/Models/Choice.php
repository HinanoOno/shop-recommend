<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use App\Models\Question;

class Choice extends Model
{
    use HasFactory;

    protected $fillable=['question_id','name','valid'];

    public function question()
    {
        return $this->belongsTo(Question::class);
    }
}
