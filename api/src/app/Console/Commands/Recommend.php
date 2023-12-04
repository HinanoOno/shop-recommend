<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;

class Recommend extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'command:recommend';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'recommend shops for users';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        logger('test');
    }
}
