<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use App\Models\Question;

class QuestionSeeder extends Seeder
{
    public function run()
    {
        $questions = [
            [
                'content' => '好きな食べ物は何でしょう？',
                'image' => 'image1.png',
                'supplement' => '冬の食べ物です',
            ],
            [
                'content' => '誕生日はいつでしょう？',
                'image' => 'image2.png',
                'supplement' => '冬生まれです',
            ],
            [
                'content' => '韓国で有名な食べ物はどれでしょう？',
                'image' => 'image3.png',
                'supplement' => '',
            ],
        ];

        foreach ($questions as $questionData) {
            Question::create($questionData);
        }
    }
}
