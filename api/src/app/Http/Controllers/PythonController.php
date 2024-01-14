<?php

//namespace App\Http\Controllers\Api\V1;
namespace App\Http\Controllers;
use Illuminate\Http\Request;
use App\Http\Requests\PythonRequest;

use App\Http\Controllers\Controller;
use Symfony\Component\Process\Exception\ProcessFailedException;
use Symfony\Component\Process\Process;


class PythonController extends Controller
{
    public function index()
    {
        $path = app_path() . "/python/main.py";
        $command = "python " . $path. " ". "俺のフレンチ";
        exec($command, $output);

        $json = json_decode($output[0]);
        return $output;
    }

    //おすすめ
    public function show($userId)
    {
        $path = app_path() . "/python/sql.py";
        $command = "python " . $path;

        exec($command, $output, $returnCode);
        return ($output);
        //return($output);
    }

    public function store(PythonRequest $request)
    {
        $keyword = $request->keyword;
        
        $path = app_path() . "/python/main.py";
        $command = "python " . $path. " ". $keyword;
        exec($command, $output);

        $json = json_decode($output[0]);

        return $json;


        // ここで必要なレスポンスを返す
        #return response()->json(['result' => $result]);
    }
}
