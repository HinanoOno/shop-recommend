<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class QuestionRequest extends FormRequest
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
            'content' => 'required|string|max:255',
            'image' => 'nullable|string|max:255',
            'supplement' => 'nullable|string|max:255',
            'choices' => 'required|array',
            'choices.*.question_id' => 'required|integer',
            'choices.*.name' => 'required|string|max:255',
            'choices.*.valid' => 'required|boolean',
        ];
    }
}
