<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class ShopResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'shop_id' => $this->shop_id,
            'name' => $this->name,
            'address' => $this->address,
            'logo_image' => $this->logo_image,
            'genre' => $this->genre,
            'url' => $this->url,
            'photo' => json_decode($this->photo), // JSON形式のデータをデコード
        ];
    }
}
