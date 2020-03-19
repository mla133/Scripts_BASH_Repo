set nocompatible
filetype plugin on
set title
set number	" show line numbers
set cursorline 	" highlight current line
set showmatch	" highlight matching [{()}]
set foldenable  " enable folding
set tabstop=4
set shiftwidth=4
set nobackup
set noswapfile
set noexpandtab

syntax on
hi Comment term=none ctermfg=green ctermbg=darkgray guifg=Gray

" Learn VIM the hard way suggested mappings {{{
" make comma new <leader>
let mapleader = ","
nnoremap <leader>ev :vsplit $MYVIMRC<CR>
nnoremap <leader>sv :source $MYVIMRC<CR>
nnoremap <leader>tt <C-]>
nnoremap <leader>rr <C-t>
nnoremap <leader>fg <C-z>
" Map <JK> key combo to emulate escape key (easier on left hand)
inoremap jk <ESC>
" }}}

" Status Line Modifications {{{
set laststatus=2	" Always show status line
set statusline=\ 
set statusline+=%f  " Current filename
set statusline+=%=	" Switch to right side
set statusline+=\ \ Line:\ %l/%L
set statusline+=\ Column:\ %c
"set statusline+=\ %y
" }}}

" CTAGS settings and mapping {{{
" Sets Vim to search directory tree for 'tags' file (for ctags)
set tags=./tags;/,tags;/
" Use CTRL-] to search tag, CTRL-T to return
" }}}

" Split Mapping and settings {{{
set splitbelow
set splitright
" }}}

" Function Key Mapping {{{
noremap <silent> <F2> :echo 'Current time is ' . strftime('%c')<CR>
noremap <silent> <F4> :!start compile.bat % & pause<CR>
noremap <silent> <F5> :!start /min build.bat & pause<CR>
noremap <silent> <F7> : <Esc>:w<CR>:!clear;lua %<CR>
noremap <silent> <F8> : <Esc>:w<CR>:!clear;scp % root@192.168.181.76:/home/root<CR>
noremap <silent> <F9> : <Esc>:w<CR>:!clear;python %<CR>
noremap <silent> <F10> : <Esc>:w<CR>:!clear;python3 %<CR>
" }}}

" Search Highlighting {{{
se hlsearch
" Ctrl-L clears the highlight from the last search
noremap <C-l> :nohlsearch<CR><C-l>
noremap! <C-l> <ESC>:nohlsearch<CR><C-l>
" }}}

" Vimscript file settings (use 'za' to fold/unfold this) {{{
augroup filetype_vim
	autocmd!
	autocmd FileType vim setlocal foldmethod=marker
augroup END
" }}}
