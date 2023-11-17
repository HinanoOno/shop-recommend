<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Shop>
 */
class ShopFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        
        return [
            'shop_id' => fake()->unique()->text(10),
            'name' => fake()->name,
            'address' => fake()->address,
            'logo_image' => fake()->imageUrl,
            'genre' => fake()->word,
            'url' => fake()->url,
            'photo' => json_encode([fake()->imageUrl, fake()->imageUrl, fake()->imageUrl]),
        ];
    }
}
