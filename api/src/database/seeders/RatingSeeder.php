<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use App\Models\User;
use App\Models\Shop;
use App\Models\Rating;


class RatingSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $users = User::factory(3)->create();
        $shops = Shop::factory(3)->create();

        foreach ($users as $user) {
            for ($i = 0; $i < 3; $i++) {
                do {
                    $shop = $shops->random();
                } while (Rating::where('user_id', $user->id)->where('shop_id', $shop->id)->exists());

                // ランダムな評価を生成
                Rating::factory()->create([
                    'user_id' => $user->id,
                    'shop_id' => $shop->id,
                ]);
            }
        }
    }
}
