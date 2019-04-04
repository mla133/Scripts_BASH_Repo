set nocompatible
filetype plugin on
"set term=ansi
set title
set number	" show line numbers
set cursorline 	" highlight current line
set showmatch	" highlight matching [{()}]
set foldenable  " enable folding
set foldmethod=syntax
set tabstop=4
set shiftwidth=4

" Status Line Modifications {{{
set laststatus=2	" Always show status line
set statusline=\ 
set statusline+=%f  " Current filename
set statusline+=%=	" Switch to right side
set statusline+=\ \ Line:\ %l/%L
set statusline+=\ Column:\ %c
"set statusline+=\ %y
" }}}

set nobackup
set noswapfile
set noexpandtab

" Split Mapping and settings {{{
set splitbelow
set splitright
" }}}

" Function Key Mapping to help with Compiling/Building {{{
noremap <silent> <F4> :!start compile.bat % & pause<CR>
noremap <silent> <F5> :!start /min build.bat & pause<CR>
noremap <silent> <F9> : <Esc>:w<CR>:!clear;python %<CR>
noremap <silent> <F11> :cd c:\Users\allenma\Desktop\GVIM\Data\settings<CR> 
noremap <silent> <F12> :cd c:\projects\legacyproducts.al3xnet\source<CR>
" }}}

syntax on
hi Comment term=none ctermfg=green ctermbg=darkgray guifg=Gray

se hlsearch
" Ctrl-L clears the highlight from the last search
noremap <C-l> :nohlsearch<CR><C-l>
noremap! <C-l> <ESC>:nohlsearch<CR><C-l>

" Vimscript file settings (use 'za' to fold/unfold this) {{{
augroup filetype_vim
	autocmd!
	autocmd FileType vim setlocal foldmethod=marker
augroup END
" }}}
