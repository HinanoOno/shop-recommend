<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use App\Models\User; 
use App\Models\Shop; 

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Rating>
 */
class RatingFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {


        return [
            'user_id' => User::factory(), // Assuming there are 10 users
            'shop_id' => Shop::factory(), // Assuming there are 10 shops
            'rating' =>  fake()->numberBetween(1, 5),
        ];
    }
}
