<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('shops', function (Blueprint $table) {
            $table->id();
            $table->string('shop_id');
            $table->string('name');
            $table->string('address')->nullable();
            $table->string('logo_image')->nullable();
            $table->string('genre')->nullable();
            $table->string('url')->nullable();
            $table->json('photo')->nullable(); // JSON形式の写真URLを格納するためのカラム
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('shops');
    }
};
