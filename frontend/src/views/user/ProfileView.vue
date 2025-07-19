<template>
  <div
    class="relative flex size-full min-h-screen flex-col bg-neutral-50 group/design-root overflow-x-hidden"
    style='font-family: "Be Vietnam Pro", "Noto Sans", sans-serif;'
  >
    <div class="layout-container flex h-full grow flex-col">
      <div class="px-40 flex flex-1 justify-center py-5">
        <div class="layout-content-container flex flex-col max-w-[960px] flex-1">
          <div class="flex p-4 @container">
            <div class="flex w-full flex-col gap-4 items-center">
              <div class="flex gap-4 flex-col items-center">
                <!-- 👤 Replaced avatar with Bootstrap person-circle -->
                <div class="text-dark">
                  <i class="bi bi-person-circle" style="font-size: 5rem;"></i>
                </div>
                <div class="flex flex-col items-center justify-center">
                  <p class="text-[#141414] text-[22px] font-bold leading-tight tracking-[-0.015em] text-center">
                    Sophia Bennett
                  </p>
                  <p class="text-neutral-500 text-base font-normal leading-normal text-center">
                    Enrolled in Data Science MasterTrack
                  </p>
                  <p class="text-neutral-500 text-base font-normal leading-normal text-center">
                    Joined in 2021
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Tabs (Removed Activity tab) -->
          <div class="pb-3">
            <div class="flex border-b border-[#dbdbdb] px-4 gap-8">
              <a
                class="flex flex-col items-center justify-center border-b-[3px] border-b-black text-[#141414] pb-[13px] pt-4"
                href="#"
              >
                <p class="text-[#141414] text-sm font-bold leading-normal tracking-[0.015em]">Overview</p>
              </a>
              <a
                class="flex flex-col items-center justify-center border-b-[3px] border-b-transparent text-neutral-500 pb-[13px] pt-4"
                href="#"
              >
                <p class="text-neutral-500 text-sm font-bold leading-normal tracking-[0.015em]">Progress</p>
              </a>
            </div>
          </div>

          <!-- Performance Summary -->
          <h2 class="text-[#141414] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">
            Performance Summary
          </h2>
          <div class="flex flex-wrap gap-4 p-4">
            <div class="flex min-w-[158px] flex-1 flex-col gap-2 rounded-xl p-6 border border-[#dbdbdb]">
              <p class="text-[#141414] text-base font-medium leading-normal">Overall Score</p>
              <p class="text-[#141414] tracking-light text-2xl font-bold leading-tight">85%</p>
            </div>
            <div class="flex min-w-[158px] flex-1 flex-col gap-2 rounded-xl p-6 border border-[#dbdbdb]">
              <p class="text-[#141414] text-base font-medium leading-normal">Courses Completed</p>
              <p class="text-[#141414] tracking-light text-2xl font-bold leading-tight">5</p>
            </div>
            <div class="flex min-w-[158px] flex-1 flex-col gap-2 rounded-xl p-6 border border-[#dbdbdb]">
              <p class="text-[#141414] text-base font-medium leading-normal">Practice Tests Taken</p>
              <p class="text-[#141414] tracking-light text-2xl font-bold leading-tight">20</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// No logic needed for static layout right now
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;700;900&family=Noto+Sans:wght@400;500;700;900&display=swap");
@import "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css";
</style>
