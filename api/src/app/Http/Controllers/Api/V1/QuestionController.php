<?php

namespace App\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use App\Http\Requests\QuestionRequest;
use App\Http\Resources\QuestionResource;
use Illuminate\Http\Request;
use App\Models\Question;
use App\Models\Choice;

class QuestionController extends Controller
{
    public function index()
    {
        return QuestionResource::collection(Question::all());
    }

    public function show(Question $quizId)
    {
        return QuestionResource::make($quizId);
    }

    public function store(QuestionRequest $request)
    {
        $questionData = $request->validated();
        $question = Question::create($questionData);

        foreach ($questionData['choices'] as $choiceData) {
            $question->choices()->create($choiceData);
        }

        return QuestionResource::make($question);
    }

    public function update(QuestionRequest $request, Question $quizId)
    {
        $quizId->update($request->validated());

        $quizId->choices()->delete();

        foreach ($request->choices as $choiceData) {
            $quizId->choices()->create($choiceData);
        }
        return QuestionResource::make($quizId);
    }

    public function destroy(Question $quizId)
    {
        $quizId->delete();

        return response()->noContent();
    }
}
