<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use App\Models\Choice;

class ChoiceSeeder extends Seeder
{
    public function run()
    {
        $choices = [
            [
                'question_id' => 1,
                'name' => '塩バターパン',
                'valid' => false,
            ],
            [
                'question_id' => 1,
                'name' => 'ラーメン',
                'valid' => false,
            ],
            [
                'question_id' => 1,
                'name' => 'みかん',
                'valid' => true,
            ],
            [
                'question_id' => 2,
                'name' => '4/5',
                'valid' => false,
            ],
            [
                'question_id' => 2,
                'name' => '9/18',
                'valid' => false,
            ],
            [
                'question_id' => 2,
                'name' => '12/30',
                'valid' => true,
            ],
            [
                'question_id' => 3,
                'name' => 'サムギョプサル',
                'valid' => true,
            ],
            [
                'question_id' => 3,
                'name' => 'どら焼き',
                'valid' => false,
            ],
            [
                'question_id' => 3,
                'name' => 'チョコパン',
                'valid' => false,
            ],
        ];

        foreach ($choices as $choiceData) {
            Choice::create($choiceData);
        }
    }
}
