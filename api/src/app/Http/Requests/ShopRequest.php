<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class ShopRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        return true;
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        return [
            'shop_id' => 'required|string',
            'name' => 'required|string|max:255',
            'address' => 'string|max:255',
            'logo_image' => 'string|max:255',
            'genre' => 'string|max:255',
            'url' => 'string|url',
            'photo' => 'json', // 配列であることを確認
            'photo.*' => 'string|url', 
        ];
    }
}
